import typehint as th
import inspect
import ast
import _ast
import subprocess
import tempfile
import ctypes
import sys

class ClowLang:
    def __init__(self, cc='cc', cflags=('-lstdc++', '-fPIC', '-shared')):
        self._cc_args = [cc] + list(cflags)
        self._functions = []

        self._types = th.TypeHints()
        self.usage = self._types.usage

    def compiled(self, f):
        self._functions.append(f)

    def _compile_functions(self, path):
        ir = '\n'.join(generate_code(f, self._types) for f in self._functions)

        with make_temp(suffix='.cpp') as cpp:
            cpp.write(ir.encode())
            cpp.flush()
            try:
                subprocess.check_output(self._cc_args + [cpp.name, '-o', path], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as ex:
                print(ex.output.decode(), file=sys.stdout)
                raise

    def compile_tempfile(self):
        with make_temp(suffix='.so', delete=False) as obj:
            self._compile_functions(obj.name)
            return obj.name

    def compile_and_load(self):
        with make_temp(suffix='.so', delete=False) as obj:
            self._compile_functions(obj.name)
            return ctypes.cdll.LoadLibrary(obj.name)

class Templates:
    FUNCTION = """
        extern "C" @ret@ @name@@args_and_body@   
    """

    ARGS_AND_BODY = """
        (@args@)
        {
            @local@@body@
        }
    """

    RETURN_VOID = "return;"
    RETURN_EXPR = "return @expr@;"

def _args(vartypes, module):
    for arg in module.args.args:
        assert type(arg) == _ast.arg
        name = arg.arg
        typename = vartypes[name]
        yield typename + ' ' + name

def _locals(vartypes, module):
    args = {arg.arg for arg in module.args.args}
    for name, typename in vartypes.items():
        if name not in args:
            yield typename + ' ' + name + ';\n'

def _assignment(vartypes, module):
    value = _generate(vartypes, module.value)
    targets = [_generate(vartypes, target) for target in module.targets]

    return ' = '.join(targets + [value]) + ';'

def _generate(vartypes, module):
    if type(module) == _ast.FunctionDef:
        stmts = ''.join(_generate(vartypes, item) for item in module.body)
        args = ', '.join(_args(vartypes, module))
        local = ''.join(_locals(vartypes, module))
        return Templates.ARGS_AND_BODY.format(args=args, local=local, body=stmts)

    if type(module) == _ast.Return:
        if module.value:
            expr = _generate(vartypes, module.value)
            return Templates.RETURN_EXPR.format(expr=expr)
        else:
            return Templates.RETURN_VOID

    if type(module) == _ast.Num:
        return str(module.n)

    if type(module) == _ast.Name:
        return module.id;

    if type(module) == _ast.Assign:
        return _assignment(vartypes, module)

    return str(type(module))

def generate_code(f, types=None):
    if types is None:
        types = th.TypeHints()

    func = th.Function(f)

    ret = types.function_returns(func)
    if ret is None:
        ret = 'void'

    vartypes = types.function_hints(func)
    args_and_body = _generate(vartypes, func.module)
    code = Templates.FUNCTION.format(ret=ret, name=func.name,
                                     args_and_body=args_and_body)

    return '\n'.join(_fix_tabs(code))

def _fix_template(template):
    opened = False
    for c in template.strip():
        if c == '@':
            yield '}' if opened else '{'
            opened = not opened
        elif c in '{}':
            yield c * 2
        else:
            yield c

def _fix_templates():
    for name in dir(Templates):
        if name[0].isupper():
            fixed = ''.join(_fix_template(getattr(Templates, name)))
            setattr(Templates, name, fixed)

def _fix_tabs(s, tab='    '):
    notabs = [line.lstrip() for line in s.split('\n')]
    shifts = 0

    for line in notabs:
        if line.startswith('}'):
            shifts -= 1
        yield (tab * shifts) + line
        if line.endswith('{'):
            shifts += 1

_fix_templates()
make_temp = tempfile.NamedTemporaryFile
