from typing import List

import functools
import warnings
import textwrap
import string, random
import collections
import hashlib
import queue

try:
    from . import zdlexer

except ImportError:
    import zdlexer


actor_list = {}

_user_var_setters = {
    'int': 'A_SetUserVar',
    'float': 'A_SetUserVarFloat',
}

_user_array_setters = {
    'int': 'A_SetUserArray',
    'float': 'A_SetUserArrayFloat',
}

def stringify(content):
    if isinstance(content, str):
        if content[0] in "'\"" and content[-1] == content[0] and len(content) > 1:
            return content

        return '"' + repr(content)[1:-1] + '"'

    return repr(content)
    
def unstringify(content):
    if content[0] in "'\"" and content[-1] == content[0] and len(content) > 1:
        return content[1:-1]

    return content

def make_id(length = 30):
    """Returns an ID, which can be stored in the ZDCode
    to allow namespace compatibility between multiple
    ZDCode mods."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def decorate(o, *args, **kwargs):
    """Get the object's compiled DECORATE code."""
    return o.__decorate__(*args, **kwargs)

def big_lit(s, indent=4, tab_size=4, strip_borders=True):
    """This function assists in the creation of
fancier triple-quoted literals, by removing
trailing indentation in lines and trailing
and leading spaces/newlines from formatting."""

    if s == "":
        return ""

    while s[0] in "\n\r": s = s[1:]
    while s[-1] in "\n\r": s = s[:-1]
    if strip_borders: s = s.strip(" \t")
    lines = s.splitlines()
    result = []

    for l in lines:
        i = indent
        while i > 0:
            if l.startswith("\t"):
                i -= tab_size
                l = l[1:]

            elif l.startswith(" "):
                i -= 1
                l = l[1:]

            else:
                break

        result.append(l)

    result = "\n".join(result)
    return result

assert big_lit("""
    YAY! I am
        Working!
""", 8) == "YAY! I am\nWorking!"

assert big_lit("""
    YAY! I am
        Working!
""", 4) == "YAY! I am\n    Working!"

assert big_lit("""
    Big
        Fluffy
    Furry.

    """, 4) == "Big\n    Fluffy\nFurry.\n"

def redent(code, spaces=8, unindent_first=True):
    b = textwrap.dedent(code).split('\n')
        
    r = []

    for l in b:
        r.append((" " * spaces) + l)

    r = "\n".join(r)

    if unindent_first: 
        return r.lstrip('\t ')

    return r

# ZDCode Classes
class ZDProperty(object):
    def __init__(self, actor, name, value):
        self.actor = actor
        self.name = name.strip()
        self.value = value

        self.actor.properties.append(self)

    def __decorate__(self):
        return "    {} {}".format(self.name, self.value)

class ZDCall(object):
    def __init__(self, code, label, func, repeats=1):
        repeats = int(repeats)

        self.func = func
        self.code = code
        self.label = label
        self.actor = label._actor
        self.repeats = repeats

        self.id = len(code.calls)

        code.calls.add(self)


        if repeats > 1:
            for _ in range(repeats):
                ZDCall(code, label, func, 1)

            del self

        elif "ZDCode_Call_{}_{}".format(code.id, self.id) not in [x.name for x in code.inventories]:
            ZDInventory(code, "ZDCode_Call_{}_{}".format(code.id, self.id))

    def post_load(self):
        if self.func in self.actor.namefuncs:
            self.actor.namefuncs[self.func].add_call(self)

    def num_states(self):
        return 2

    def __decorate__(self):
        func = self.actor.namefuncs[self.func]

        return redent(
            "    TNT1 A 0 A_GiveInventory(\"ZDCode_Call_{2}_{1}\")\n" +
            "    Goto ZDCode_Func_{0}\n" +
            "ZDCode_CLabel{1}:\n" + 
            "    TNT1 A 0 A_TakeInventory(\"ZDCode_Call_{2}_{1}\")",
        4, unindent_first = False).format(func.name, self.id, self.code.id)

class ZDFunction(object):
    def __init__(self, code, actor, name, states=None):
        if not states:
            states = []

        self.code = code
        self.name = name.strip()
        self.states = states
        self.calls = []
        self.actor = actor

        self.id = len(actor.all_funcs)
        actor.funcs.append((name, self))
        actor.namefuncs[name] = self
        actor.all_funcs.append((name, self))

    def add_call(self, call):
        self.calls.append(call)

    def call_states(self):
        result = []

        for c in self.calls:
            result.append("TNT1 A 0 A_JumpIfInventory(\"ZDCode_Call_{1}_{0}\", 1, \"ZDCode_CLabel{0}\")".format(c.id, self.code.id))

        return ("    " + redent("\n".join(result), 4) if len(result) > 0 else "")

    def state_code(self):
        r = ""

        for s in self.states:
            if type(s) in (ZDState, ZDRawDecorate):
                r += "    {}\n".format(decorate(s))

            else:
                r += "{}\n".format(decorate(s))

        return r[:-1]

    def label_name(self):
        return "ZDCode_Func_" + self.name

    def __decorate__(self):
        code = "    ZDCode_Func_{}:".format(self.name)
        code += '\n' + self.state_code()

        cst = self.call_states()

        if cst != '':
            code += '\n' + cst

        code += "\n    TNT1 A -1\n    Stop"

        return code

class ZDState(object):
    def __init__(self, sprite='"####"', frame='"#"', duration=0, keywords=None, action=None):
        if not keywords:
            keywords = []

        self.sprite = sprite
        self.frame = frame
        self.keywords = keywords
        self.action = action
        self.duration = duration

    def num_states(self):
        return 1

    def __decorate__(self):
        if self.keywords:
            keywords = [" "] + self.keywords

        else:
            keywords = []

        action = ""
        if self.action:
            action = " " + str(self.action)

        return "{} {} {}{}{}".format(
            self.sprite.upper(),
            self.frame.upper(),
            str(self.duration),
            " ".join(keywords),
            action
        )

class ZDLabel(object):
    def __init__(self, _actor, name, states=None, auto_append=True):
        if not states:
            states = []

        self.name = name.strip()
        self.states = states
        self._actor = _actor

        if auto_append:
            self._actor.labels.append(self)

    def __repr__(self):
        return "{}({} of {})".format(type(self).__name__, self.name, repr(self._actor.name))

    def label_name(self):
        return self.name

    def add_state(self, state):
        self.states.append(state)

    def __decorate__(self):
        if self.name.startswith("F_"):
            self.name = "_" + self.name

        r = "{}:".format(self.name)

        for s in self.states:
            if type(s) in (ZDState, ZDRawDecorate):
                r += "\n    {}".format(decorate(s))

            else:
                r += "\n{}".format(decorate(s))

        return r

class ZDReturnStatement(object):
    def __init__(self, func):
        self.func = func

    def num_states(self):
        return len(self.func.calls)

    def __decorate__(self):
        return big_lit(self.func.call_states() + "\n    Stop", 4)

class ZDRawDecorate(object):
    def __init__(self, raw):
        self.raw = raw

    def num_states(self):
        return 0

    def __decorate__(self):
        return self.raw

class ZDBaseActor(object):
    def __init__(self, code, name=None, inherit=None, replace=None, doomednum=None, _id=None):
        self.code = code
        self.name = name.strip()
        self.inherit = inherit
        self.replace = replace
        self.num = doomednum
        self.id = _id or make_id(30)
        
class ZDActor(ZDBaseActor):
    def __init__(self, code, name, inherit=None, replace=None, doomednum=None, _id=None, context=None):
        if context:
            self.context = context.derive()

        else:
            self.context = ZDCodeParseContext()

        ZDBaseActor.__init__(self, code, name, inherit, replace, doomednum, _id)

        self.labels = []
        self.properties = []
        self.flags = set()
        self.uservars = []
        self.antiflags = set()
        self.funcs = []
        self.namefuncs = {}
        self.raw = []

        if self.inherit and self.inherit.upper() in code.actor_names:
            self.all_funcs = list(code.actor_names[self.inherit.upper()].all_funcs)
            self.context.update(code.actor_names[self.inherit.upper()].context)

        else:
            self.all_funcs = []

        # code.actor_names[name.upper()] = self

    def make_spawn_label(self):
        return ZDLabel(self, 'Spawn', [ZDRawDecorate('goto Super::Spawn' if self.inherit else 'stop')], auto_append=False)

    def get_spawn_label(self):
        for l in self.labels:
            if l.name.upper() == 'SPAWN':
                return l

        return None

    def _set_user_var_state(self, var):
        vtype, vlit = var['value']

        if vtype == 'val':
            return [ZDState(action='{}({}, {})'.format(_user_var_setters[var['type']], stringify(var['name']), vlit))]

        elif vtype == 'arr':
            return [ZDState(action='{}({}, {}, {})'.format(_user_array_setters[var['type']], stringify(var['name']), i, v)) for i, v in enumerate(vlit)]

    def _get_spawn_prelude(self):
        return sum([self._set_user_var_state(var) for var in self.uservars if var.get('value', None)], [])

    def prepare_spawn_label(self):
        label = self.get_spawn_label()

        if self.uservars:
            if not label:
                label = self.make_spawn_label()

            label.states = [ZDState("TNT1", "A")] + self._get_spawn_prelude() + label.states

        elif label:
            label.states.insert(0, ZDState("TNT1", "A"))

    def get_context(self):
        return self.context

    def top(self):
        r = []

        for p in sorted(self.properties, key=lambda p: p.name):
            r.append(decorate(p))

        r.append("")

        for u in self.uservars:
            r.append('var {} {}{};'.format(u['type'], u['name'], '[{}]'.format(u['size']) if u.get('size', 0) else ''))

        for f in self.flags:
            r.append("+{}".format(f))

        for a in self.antiflags:
            r.append("-{}".format(a))

        for rd in self.raw:
            r.append(rd)

        if len(r) == 1 and r[0] == "":
            return "    "

        return redent(big_lit("\n".join(r), 8), 4, False)

    def label_code(self):
        r = []

        for f in self.funcs:
            r.append(decorate(f[1]))

        for l in self.labels:
            r.append(decorate(l))

        return redent("\n\n".join(r), 8, False)

    def header(self):
        r = self.name

        if self.inherit: r += " : {}".format(self.inherit)
        if self.replace: r += " replaces {}".format(self.replace)
        if self.num:     r += " {}".format(str(self.num))

        return r

    def __decorate__(self):
        if self.labels + self.funcs:
            t = self.top()
            return big_lit(
            """Actor {}
            {{
            {}
                States {{
                    {}
                }}
            }}""", 12).format(self.header(), redent(t, 4, unindent_first=False), redent(self.label_code(), unindent_first=True))

        return big_lit(
        """
        Actor {}
        {{
        {}
        }}""", 8).format(self.header(), redent(self.top(), 4, unindent_first=False))

class ZDClassTemplate(ZDBaseActor):
    def __init__(self, template_parameters, parse_data, abstract_label_names, abstract_macro_names, abstract_array_names, group_name, code, name, inherit=None, replace=None, doomednum=None, _id=None):
        ZDBaseActor.__init__(self, code, name, inherit, replace, doomednum, _id)

        self.group_name = group_name or None

        self.template_parameters = list(template_parameters)

        self.abstract_label_names = set(abstract_label_names)
        self.abstract_macro_names = dict(abstract_macro_names)
        self.abstract_array_names = dict(abstract_array_names)

        self.parse_data = parse_data
        self.parametric_table = {}

    def generated_class_name(self, parameter_values, new_id):
        hash = hashlib.sha1()

        hash.update(self.name.encode('utf-8'))
        hash.update(self.id.encode('utf-8'))
        hash.update(new_id.encode('utf-8'))

        for parm in parameter_values:
            hash.update(parm.encode('utf-8'))

        for name in self.abstract_label_names:
            hash.update(name.encode('utf-8'))

        for name, args in self.abstract_macro_names.items():
            hash.update(name.encode('utf-8'))

            for arg in args:
                hash.update(arg.encode('utf-8'))

        return '{}__deriv_{}'.format(self.name, hash.hexdigest())

    def generate_init_class(self, code, context, parameter_values, provided_label_names=(), provided_macro_names=(), provided_array_names=(), name=None, pending=None):
        if tuple(parameter_values) in self.parametric_table and not self.abstract_label_names and not self.abstract_macro_names and not self.abstract_array_names:
            return (False, self.parametric_table[tuple(parameter_values)])

        provided_label_names = set(provided_label_names)
        provided_macro_names = dict(provided_macro_names)

        new_name = name if name is not None else self.generated_class_name(parameter_values, make_id(40))

        if self.group_name:
            self.code.groups[self.group_name].append(stringify(new_name))

        inh = self.inherit and context.replacements.get(self.inherit.upper(), self.inherit) or None
        rep = self.replace and context.replacements.get(self.replace.upper(), self.replace) or None

        res = ZDActor(self.code, new_name, inh, rep, self.num, context=context)

        for l in self.abstract_label_names:
            if l not in provided_label_names:
                raise CompilerError("Tried to derive template {} in {}, but abstract label {} does not have a definition!".format(self.name, context.describe(), l))

        for m, a in self.abstract_macro_names.items():
            if m not in provided_macro_names.keys():
                raise CompilerError("Tried to derive template {} in {}, but abstract macro {} does not have a definition!".format(self.name, context.describe(), m))

            if len(a) != len(provided_macro_names[m]):
                raise CompilerError("Tried to derive template {} in {}, but abstract macro {} has the wrong number of arguments: expected {}, got {}!".format(self.name, context.describe(), m, len(a), len(provided_macro_names[m])))

        for m, a in self.abstract_array_names.items():
            if m not in provided_array_names.keys():
                raise CompilerError("Tried to derive template {} in {}, but abstract array {} is not defined!".format(self.name, context.describe(), m))

            if a['size'] != 'any' and a['size'] != provided_array_names[m]:
                raise CompilerError("Tried to derive template {} in {}, but abstract array {} has a size constraint; expected {} array elements, got {}!".format(self.name, context.describe(), m, a['size'], provided_array_names[m]))

        self.parametric_table[tuple(parameter_values)] = res

        return (True, res)

    def get_init_replacements(self, code, context, parameter_values):
        return dict(zip((p.upper() for p in self.template_parameters), parameter_values))

class ZDBlock(object):
    def __init__(self, actor, states = ()):
        self._actor = actor
        self.states = list(states)

    def num_states(self):
        return sum(x.num_states() for x in self.states)

    def __decorate__(self):
        return redent('\n'.join(decorate(x) for x in self.states), 4, unindent_first=False)

class ZDIfStatement(object):
    def __init__(self, actor, condition, states = ()):
        self._actor = actor
        self.true_condition = condition
        self.states = list(states)
        self.else_block = None

    def set_else(self, else_block):
        self.else_block = else_block

    def num_block_states(self):
        return sum(x.num_states() for x in self.states)

    def num_else_states(self):
        return self.else_block.num_states()

    def num_states(self):
        if self.else_block:
            return self.num_block_states() + self.num_else_states() + 3

        else:
            return self.num_block_states() + 2

    def __decorate__(self):
        num_st_bl = self.num_block_states()
        
        if self.else_block:
            num_st_el = self.num_else_states()

            return redent(
                "TNT1 A 0 A_JumpIf({}, {})\n".format(self.true_condition, num_st_el + 2) +      # 1
                decorate(self.else_block) +                                                     # + num_st_el
                "\nTNT1 A 0 A_Jump(256, {})\n".format(num_st_bl + 1) +                          # + 1
                '\n'.join(decorate(x) for x in self.states) +                                   # + num_st_bl
                "\nTNT1 A 0",                                                                   # + 1
            4, unindent_first=False)

        else:
            return redent(
                "TNT1 A 0 A_JumpIf(!({}), {})\n".format(self.true_condition, num_st_bl + 1) +   # 1
                '\n'.join(decorate(x) for x in self.states) +                                   # + num_st_bl
                "\nTNT1 A 0",                                                                   # + 1
            4, unindent_first=False)


class ZDIfJumpStatement(object):
    def __init__(self, actor, condition_gen, states = ()):
        self._actor = actor
        self.true_condition = condition_gen
        self.states = list(states)
        self.else_block = None

    def set_else(self, else_block):
        self.else_block = else_block

    @classmethod
    def generate(cls, actor, states = ()):
        def _decorator(condition_gen):
            return cls(actor, condition_gen, states)

        return _decorator

    def num_block_states(self):
        return sum(x.num_states() for x in self.states)

    def num_else_states(self):
        return self.else_block.num_states()

    def num_states(self):
        if self.else_block:
            return self.num_block_states() + self.num_else_states() + 3

        else:
            return self.num_block_states() + 3

    def __decorate__(self):
        num_st_bl = self.num_block_states()
        
        if self.else_block:
            num_st_el = self.num_else_states()

            return redent(
                "TNT1 A 0 {}\n".format(self.true_condition(num_st_el + 2)) +                # 1
                decorate(self.else_block) +                                                 # + num_st_el
                "\nTNT1 A 0 A_Jump(256, {})\n".format(num_st_bl + 1) +                      # + 1
                '\n'.join(decorate(x) for x in self.states) +                               # + num_st_bl
                "\nTNT1 A 0",                                                               # + 1
            4, unindent_first=False)

        else:
            return redent(
                "TNT1 A 0 {}".format(self.true_condition(2)) +                              # 1
                "\nTNT1 A 0 A_Jump(256, {})\n".format(num_st_bl + 1) +                      # + 1
                '\n'.join(decorate(x) for x in self.states) +                               # + num_st_bl
                "\nTNT1 A 0",                                                               # + 1
            4, unindent_first=False)


class ZDSometimes(object):
    def __init__(self, actor, chance, states):
        self._actor = actor
        self.chance = chance
        self.states = states

    def num_states(self):
        return sum(x.num_states() for x in self.states) + 2

    def __decorate__(self):
        num_st = sum(x.num_states() for x in self.states)

        return redent("TNT1 A 0 A_Jump(256-(256*({})/100), {})\n".format(self.chance, num_st + 1) + '\n'.join(decorate(x) for x in self.states) + "\nTNT1 A 0", 4, unindent_first=False)

num_whiles = 0

class ZDWhileStatement(object):
    def __init__(self, actor, condition, states = ()):
        self._actor = actor
        self.true_condition = condition
        self.states = list(states)
        self.else_block = None

        global num_whiles
        
        self._while_id = num_whiles
        num_whiles += 1

        self._loop_id = '_loop_while_' + str(self._while_id)

    def set_else(self, else_block):
        self.else_block = else_block

    def num_block_states(self):
        return sum(x.num_states() for x in self.states)

    def num_else_states(self):
        return self.else_block.num_states()

    def num_states(self):
        if self.else_block:
            return self.num_block_states() + self.num_else_states() + 4

        else:
            return self.num_block_states() + 3

    def __decorate__(self):
        num_st_bl = self.num_block_states()
        
        if self.else_block:
            num_st_el = self.num_else_states()

            return redent(
                "TNT1 A 0 A_JumpIf({}, {})\n".format(self.true_condition, num_st_el + 2) +              # 1
                decorate(self.else_block) +                                                             # + num_st_el
                "\nTNT1 A 0 A_Jump(256, {})".format(num_st_bl + 2) +                                    # + 1
                "\n{}:\n".format(self._loop_id) +                                                       # |
                '\n'.join(decorate(x) for x in self.states) +                                           # + num_st_bl
                "\nTNT1 A 0 A_JumpIf({}, {})".format(self.true_condition, stringify(self._loop_id)) +   # + 1
                "\nTNT1 A 0",                                                                           # + 1
            4, unindent_first=False)

        else:
            return redent(
                "TNT1 A 0 A_JumpIf(!({}), {})".format(self.true_condition, num_st_bl + 2) +             # 1
                "\n{}:\n".format(self._loop_id) +                                                       # |
                '\n'.join(decorate(x) for x in self.states) +                                           # + num_st_bl
                "\nTNT1 A 0 A_JumpIf({}, {})".format(self.true_condition, stringify(self._loop_id)) +   # + 1
                "\nTNT1 A 0",                                                                           # + 1
            4, unindent_first=False)


class ZDWhileJumpStatement(object):
    def __init__(self, actor, condition_gen, states = ()):
        self._actor = actor
        self.true_condition = condition_gen
        self.states = list(states)
        self.else_block = None

        global num_whiles
                
        self._while_id = num_whiles
        num_whiles += 1

        self._loop_id = '_loop_while_' + str(self._while_id)

    def set_else(self, else_block):
        self.else_block = else_block

    @classmethod
    def generate(cls, actor, states = ()):
        def _decorator(condition_gen):
            return cls(actor, condition_gen, states)

        return _decorator

    def num_block_states(self):
        return sum(x.num_states() for x in self.states)

    def num_else_states(self):
        return self.else_block.num_states()

    def num_states(self):
        if self.else_block:
            return self.num_block_states() + self.num_else_states() + 4

        else:
            return self.num_block_states() + 4

    def __decorate__(self):
        num_st_bl = self.num_block_states()

        if self.else_block:
            num_st_el = self.num_else_states()

            return redent(
                "TNT1 A 0 {}\n".format(self.true_condition(num_st_el + 2)) +                            # 1
                decorate(self.else_block) +                                                             # + num_st_el
                "\nTNT1 A 0 A_Jump(256, {})".format(num_st_bl + 2) +                                    # + 1
                "\n{}:\n".format(self._loop_id) +                                                       # |
                '\n'.join(decorate(x) for x in self.states) +                                           # + num_st_bl
                "\nTNT1 A 0 {}".format(self.true_condition(stringify(self._loop_id))) +                 # + 1
                "\nTNT1 A 0",                                                                           # + 1
            4, unindent_first=False)

        else:
            return redent(
                "TNT1 A 0 {}".format(self.true_condition(2)) +                                          # 1
                "\nTNT1 A 0 A_Jump(256, {})\n".format(num_st_bl + 2) +                                  # + 1
                "\n{}:\n".format(self._loop_id) +                                                       # |
                '\n'.join(decorate(x) for x in self.states) +                                           # + num_st_bl
                "\nTNT1 A 0 {}".format(self.true_condition(stringify(self._loop_id))) +                 # + 1
                "\nTNT1 A 0",                                                                           # + 1
            4, unindent_first=False)


class ZDInventory(object):
    def __init__(self, code, name):
        self.name = name.strip()
        self.code = code

        code.inventories.append(self)

    def __decorate__(self):
        return "Actor {} : Inventory {{Inventory.MaxAmount 1}}".format(self.name)
        
        
class ZDSkip:
    def __init__(self, code, skip_context, curr_ind):
        self.code = code
        self.context = skip_context
        self.ind = curr_ind
        
    def __decorate__(self):
        return 'TNT1 A 0 A_Jump(256, {})'.format(self.context.num_states() - self.ind + 1)
        
    def num_states(self):
        return 1

# Compiler!
class CompilerError(Exception):
    pass

class ZDCodeParseContext(object):
    def __init__(self, replacements=(), macros=(), templates=(), calls=(), actors=(), remote_offset=0):
        self.includes = {}
        self.macros = dict(macros)
        self.replacements = dict(replacements)
        self.templates = dict(templates)
        self.call_lists = list(calls) if calls else [[]]
        self.actor_lists = list(actors) if actors else [[]]
        self.desc_stack = []
        self.states = []
        self.remote_children = []
        self.remote_offset = remote_offset
        
    def print_state_tree(self, _print_low=print, _print=print, prefix='+ '):
        ended = 0
        
        _print_low = _print_low or print
        
        def _print_top(name):
            _print_low(prefix + name)
            
        def _branch(l='', end=False):
            if end:
                _print("'---+ " + l)
            
            else:
                _print("+---+ " + l)
                
        def _print_next(line=''):
            if ended == 0:
                _print('|   ' + line)
                
            elif ended == 1 and self.remote_children:
                _print(':   ' + line)
            
            else:
                _print('    ' + line)
    
        _print_top('{} ({}/{})'.format(self.desc_stack[-1], self.num_states(), self.remote_num_states()))
        
        if self.states:
            _print('|')
            
            imax = len(self.states)
            
            for i, s in enumerate(self.states):
                ended = 1 if i >= imax - 1 else 0
            
                if isinstance(s, ZDCodeParseContext):
                    s.print_state_tree(_print, _print_next, "'---+ " if ended > 0 else "+---+ ")
                    
                else:
                    _branch('{} ({})'.format(type(s).__name__, s.num_states()), ended)
                    
                if not ended:
                    _print('|')
            
        if self.remote_children:
            _print('&')
            _print(':')
            
            imax = len(self.remote_children)
            
            for i, ch in enumerate(self.remote_children):
                ended = 2 if i >= imax - 1 else 1
                
                ch.print_state_tree(_print, _print_next, "^---* (remote) " if ended > 1 else "%---* (remote) ")
                
                if not ended:
                    _print(':')
        
    def num_states(self):
        return sum(s.num_states() for s in self.states)
        
    def remote_num_states(self):
        return self.remote_offset + sum(s.remote_num_states() if isinstance(s, ZDCodeParseContext) else s.num_states() for s in self.states) + sum(c.remote_num_states() for c in self.remote_children)

    def remote_derive(self, desc: str = None, remote_offset: int = 0) -> "ZDCodeParseContext":
        # derives without adding to states
        res = ZDCodeParseContext(self.replacements, self.macros, self.templates, self.call_lists, self.actor_lists, remote_offset)
        res.desc_stack = list(self.desc_stack)
        
        if desc:
            res.desc_stack.append(desc)
            
        self.remote_children.append(res)
        
        return res

    def derive(self, desc: str = None) -> "ZDCodeParseContext":
        res = ZDCodeParseContext(self.replacements, self.macros, self.templates, self.call_lists, self.actor_lists)
        res.desc_stack = list(self.desc_stack)
        
        if desc:
            res.desc_stack.append(desc)
            
        self.states.append(res)
        
        return res
        
    def __repr__(self):
        return 'ZDCodeParseContext({})'.format(self.repr_describe())
        
    def desc_block(self, desc: str):
        return ZDCtxDescBlock(self, desc)

    def update(self, other_ctx: "ZDCodeParseContext"):
        self.macros.update(other_ctx.macros)
        self.replacements.update(other_ctx.replacements)
        self.templates.update(other_ctx.templates)

    def add_call(self, c: ZDCall):
        for cl in self.call_lists:
            cl.append(c)

    def add_actor(self, ac: ZDActor):
        for al in self.actor_lists:
            al.append(ac)
            
    def describe(self):
        return ' at '.join(self.desc_stack[::-1])
        
    def repr_describe(self):
        return ', '.join(self.desc_stack[::-1])
        
    def resolve(self, name, desc = 'a parametrizable name'):
        while name[0] == '@':
            resolves = len(name) - len(name.lstrip('@'))
            casename = name[resolves:]
            name = name[resolves:].upper()

            if name in self.replacements:
                if resolves > 1:
                    name = '@' * (resolves - 1) + self.replacements[name]
                
                else:
                    name = self.replacements[name]

            else:
                raise CompilerError("No such replacement {} while trying to resolve {} in {}!".format(repr(casename), self.describe()))
                
        return name

@functools.total_ordering
class PendingTask:
    def __init__(self, priority, func):
        self.priority = priority
        self.func = func
        
    def __lt__(self, other):
        return self.priority < other.priority
        
    def __eq__(self, other):
        return self.priority == other.priority

def pending_task(priority):
    def _decorator(func):
        return PendingTask(priority, func)
        
    return _decorator

class ZDCtxDescBlock:
    def __init__(self, ctx, desc):
        self.ctx = ctx
        self.desc = desc

    def __enter__(self):
        self.ctx.desc_stack.append(self.desc)
        
    def __exit__(self, _1, _2, _3):
        assert self.ctx.desc_stack.pop() == self.desc

class ZDCode(object):
    class ZDCodeError(BaseException):
        pass

    @classmethod
    def parse(cls, code, fname=None, dirname='.', error_handler=None):
        data = zdlexer.parse_code(code.strip(' \t\n'), dirname=dirname, filename=fname, error_handler=error_handler, imports=self.includes)

        if data:
            res = cls()
            
            try:
                res._parse(data)
                
            except CompilerError as err:
                if error_handler: error_handler(err)
                return None

            return res

        else:
            return None

    def add(self, code, fname=None, dirname='.', error_handler=None):
        data = zdlexer.parse_code(code.strip(' \t\n'), dirname=dirname, filename=fname, error_handler=error_handler)

        if data:
            try:
                self._parse(data)
                
            except CompilerError as err:
                if error_handler: error_handler(err)
                return False

        return bool(data)

    def _parse_expression(self, expr, context):
        etype, exval = expr

        if etype == 'expr':
            return ' '.join(self._parse_expression(item, context) for item in exval)

        elif etype == 'literal':
            return self._parse_literal(exval, context)

        elif etype == 'array index':
            return '[' + self._parse_expression(exval, context) + ']'

        elif etype == 'oper':
            return exval

        elif etype == 'paren expr':
            return '(' + self._parse_expression(exval, context) + ')'

    def _parse_argument(self, arg, context, name = None):
        atype, aval = arg

        if atype == 'position arg':
            return self._parse_parameter(aval, context, name)

    def _parse_parameter(self, parm, context, name = None):
        ptype, pval = parm

        if ptype == 'expression':
            return self._parse_expression(pval, context)

        elif ptype == 'template derivation':
            return self._parse_template_derivation(pval, context)

        elif ptype == 'anonymous class':
            return self._parse_anonym_class(pval, context)
            
        elif ptype == 'anonymous macro':
            return self._parse_anonym_macro(*pval, context, name)

    def _parse_anonym_macro(self, args, body, context, name = None):
        name = name or 'ANONYMMACRO_{}_{}'.format(self.id.upper(), self.num_anonym_macros)
        self.num_anonym_macros += 1
        
        context.macros[name.upper()] = (args, body)
        
        return stringify(name)

    def _parse_literal(self, literal, context):
        if isinstance(literal, str):
            return literal

        if literal[0] == 'number':
            return str(literal[1])

        elif literal[0] == 'string':
            return '"' + repr(literal[1])[1:-1] + '"'

        elif literal[0] == 'actor variable':
            if literal[1].upper() in context.replacements:
                return context.replacements[literal[1].upper()]

            else:
                return literal[1]

        elif literal[0] == 'call expr':
            return self._parse_action(literal[1], context)

        elif literal[0] == 'anonymous class':
            return self._parse_anonym_class(literal[1], context)

        elif literal[0] == 'template derivation':
            return self._parse_template_derivation(literal[1])

    def _parse_array(self, arr, context):
        arr = dict(arr)
        arr['value'] = ('array', [self._parse_expression(e, context) for e in arr['value'][1]])

        return arr

    def _parse_template_derivation(self, deriv, context, pending=None, name=None, stringify=True):
        template_name, template_parms, deriv_body = deriv
        
        try:
            template = context.templates[template_name]

        except KeyError:
            raise CompilerError("Unknown template '{}' to derive in {}".format(template_name, context.describe()))
        
        if len(template_parms) != len(template.template_parameters):
            raise CompilerError("Bad number of template parameters for '{}' in {}: expected {}, got {}".format(
                template_name,
                context.describe(),
                len(template.template_parameters),
                len(template_parms)
            ))

        template_parms = [self._parse_parameter(a, context, template.template_parameters[i]) for i, a in enumerate(template_parms)]
        template_labels = {}
        template_body = []
        template_macros = {}
        template_arrays = {}

        for btype, bdata in deriv_body:
            if btype == 'array':
                bdata = self._parse_array(bdata, context)
                template_arrays[bdata['name']] = bdata

            elif btype == 'label':
                template_labels[bdata['name']] = bdata

            elif btype == 'macro':
                template_macros[bdata['name']] = bdata
                
            template_body.append((btype, bdata))

        new_class = self._derive_class_from_template(template, template_parms, context, template_labels, template_macros, template_arrays, template_body, pending=pending, name=name)

        if stringify:
            return '"' + repr(new_class.name)[1:-1] + '"'

        else:
            return new_class

    def _parse_action(self, a, context):
        aname = a[0]
        aname = context.replacements.get(aname.upper(), aname)

        args = list(a[1]) if a[1] else []
        args = [(context.replacements.get(x.upper(), x) if isinstance(x, str) else x) for x in args]
        args = [self._parse_argument(x, context) for x in args]
        args = ', '.join(a for a in args if a)

        return "{}({})".format(aname, args)

    def _parse_state_action_or_body(self, a, context):
        if a[0] == 'action':
            return [self._parse_state_action(a[1], context)]

        elif a[0] == 'inline body':
            res = []

            for x in a[1]:
                res.extend(self._parse_state_action_or_body(x, context))

            return res
            
        elif a[0] == 'repeated inline body':
            res = []

            cval, xidx, body = a[1]
            count = self._parse_replaceable_number(cval, context)

            if count >= 1:
                for idx in range(count):
                    ctx = context.derive()
                
                    if xidx:
                        ctx.replacements[xidx] = str(idx)
                
                    res.extend(self._parse_state_action_or_body(body, ctx))
                        
            return res

    def _parse_state_action(self, a, context):
        args = list(a[1]) if a[1] else []
        args = [self._parse_argument(x, context) for x in args]
        args = [(context.replacements.get(x.upper(), x) if isinstance(x, str) else x) for x in args]
        args = ', '.join(a for a in args if a)

        if len(args) > 0:
            return "{}({})".format(a[0], args)

        else:
            return a[0]

    def _parse_replaceable_number(self, cval, context: ZDCodeParseContext):
        if isinstance(cval, str):
            cval = context.replacements.get(cval.upper(), cval)

        try:
            count = int(cval)

        except ValueError:
            raise CompilerError("Invalid repeat count in {}: expected valid integer, got {}".format(context.describe(), repr(cval)))

        else:
            return count
    
    def _mutate_block(self, mut_func, block, *args):
        return [mut_func(s, *args) for s in block]
            
    def _maybe_mutate_block(self, mut_func, state, *args):
        state = list(state)
    
        if state[0] == 'ifjump':
            jump, s_yes, s_no = state[1]
            state[1] = (jump, self._mutate_block(mut_func, s_yes, *args), s_no and self._mutate_block(mut_func, s_no, *args))
            
        elif state[0] == 'if':
            cond, s_yes, s_no = state[1]
            state[1] = (cond, self._mutate_block(mut_func, s_yes, *args), s_no and self._mutate_block(mut_func, s_no, *args))
            
        elif state[0] == 'sometimes':
            state[1] = dict(state[1])
            state[1]['body'] = self._mutate_block(mut_func, state[1]['body'], *args)
        
        return state
        
    def _maybe_mutate_block_or_loop(self, mut_func, state, *args):
        state = list(state)
    
        if state[0] in ('while', 'whilejump'):
            cond, f_body, f_else = state[1]
            
            f_body = self._mutate_block(mut_func, f_body, *args)
            f_else = f_else and self._mutate_block(mut_func, f_else, *args)
            
            state[1] = (cond, f_body, f_else)
            
        elif state[0] == 'for':
            itername, iteridx, itermode, f_body, f_else = state[1]
            
            f_body = self._mutate_block(mut_func, f_body, *args)
            f_else = f_else and self._mutate_block(mut_func, f_else, *args)
            
            state[1] = (itername, iteridx, itermode, f_body, f_else)
        
        return self._maybe_mutate_block(mut_func, state, *args)
            
    def _mutate_macro_state(self, state, inj_context):
        # Mutates each state in an injected macro, making things
        # like macro-scope return statements possible.
        
        if state[0] == 'return':
            return ('skip', inj_context)
        
        return self._maybe_mutate_block_or_loop(self._mutate_macro_state, state, inj_context)
        
    def _mutate_iter_state(self, state, break_context, loop_context):
        # Mutates each state in a for loop, making things like
        # break and continue statements possible.
        
        if state[0] == 'continue':
            return ('skip', loop_context)
            
        if state[0] == 'break':
            return ('skip', break_context)
        
        return self._maybe_mutate_block(self._mutate_iter_state, state, break_context, loop_context)

    def _parse_state(self, actor, context: ZDCodeParseContext, label, s, func=None, alabel=None):
        def add_state(s, target=context):
            target.states.append(s)
            label.states.append(s)
            
            return s
            
        def pop_remote(target=context):
            assert target.remote_children
            target.remote_children.pop()
            
        def clear_remotes(target=context):
            target.remote_children.clear()
    
        if s[0] == 'frames':        
            (sprite_type, sprite_name), frames, duration, modifier_chars, action = s[1]
            modifiers = []
            
            for mod in modifier_chars:
                res = ''
            
                for ctype, cval in mod:
                    if ctype == 'replace':
                        try:
                            cval = context.replacements[cval.upper()]

                        except KeyError:
                            raise CompilerError("No parameter {} for replacement within modifier, in {}!".format(context.describe()))

                    res += cval

            if sprite_type == 'normal':
                name = sprite_name

            elif sprite_type == 'parametrized':
                try:
                    new_name = context.replacements[sprite_name.upper()]

                    if new_name[0] == "'" and new_name[-1] == "'":
                        new_name = new_name[1:-1]

                    elif new_name[0] == '"' and new_name[-1] == '"':
                        new_name = new_name[1:-1]

                    else:
                        raise CompilerError("Parametrized sprite '{}' in {} needs to be passed a string; got {}".format(sprite_name, context.describe(), repr(new_name)))

                    name = new_name

                except KeyError:
                    raise CompilerError("No parameter {} for parametrized sprite name, in {}!".format(repr(sprite_name), context.describe()))

            if frames == '"#"':
                frames = ['"#"']

            for f in frames:
                if action is None:
                    add_state(ZDState(name, f, duration, modifiers))

                else:
                    body = self._parse_state_action_or_body(action, context)

                    for i, a in enumerate(body):
                        add_state(ZDState(name, f, (0 if i + 1 < len(body) else duration), modifiers, action=a))

        elif s[0] == 'return':
            if not isinstance(func, ZDFunction):
                raise CompilerError("Return statements are not valid in {}!".format(context.describe()))

            else:
                add_state(ZDReturnStatement(func))
                
        elif s[0] == 'continue':
            raise CompilerError("Continue statements are not valid in {}!".format(context.describe()))
            
        elif s[0] == 'break':
            raise CompilerError("Break statements are not valid in {}!".format(context.describe()))
                
        elif s[0] == 'skip':
            # Skips to the end of this context, or the one supplied.
            if s[1]:
                # s[1] can only be an outer context, so don't bother checking
                add_state(ZDSkip(self, s[1], s[1].remote_num_states()))
            
            else:
                add_state(ZDSkip(self, context, context.remote_num_states()))

        elif s[0] == 'call':
            context.add_call(add_state(ZDCall(self, label, s[1])))

        elif s[0] == 'flow':
            if s[1].upper().rstrip(';') == 'LOOP':
                add_state(ZDRawDecorate('goto {}'.format(label.name)))

            else:
                sf    = s[1].rstrip(';').split(' ')
                sf[0] = sf[0].lower()
                
                add_state(ZDRawDecorate(' '.join(sf)))

        elif s[0] == 'repeat':
            cval, xidx, body = s[1]

            break_ctx = context.derive()
            count = self._parse_replaceable_number(cval, context)

            if count >= 1:
                for idx in range(count):
                    loop_ctx = break_ctx.derive()
                
                    if xidx:
                        loop_ctx.replacements[xidx.upper()] = str(idx)
                
                    for a in body:
                        self._parse_state(actor, loop_ctx, label, self._mutate_iter_state(a, break_ctx, loop_ctx), func)

        elif s[0] == 'sometimes':
            s = dict(s[1])

            chance = self._parse_expression(s['chance'], context)
            sms = ZDSometimes(actor, chance, [])

            for a in s['body']:
                self._parse_state(actor, context, sms, a, func)

            add_state(sms)

        elif s[0] == 'if':
            ifs = ZDIfStatement(actor, self._parse_expression(s[1][0], context), [])
            if_ctx = context.remote_derive('if body', 3 if s[1][2] else 2)

            for a in s[1][1]:
                self._parse_state(actor, if_ctx, ifs, a, func)

            if s[1][2]:
                elses = ZDBlock(actor)

                for a in s[1][2]:
                    self._parse_state(actor, if_ctx, elses, a, func)

                ifs.set_else(elses)

            add_state(ifs)
            pop_remote()

        elif s[0] == 'ifjump':
            jump, s_yes, s_no = s[1]
        
            @ZDIfJumpStatement.generate(actor)
            def ifs(jump_offset):
                jump_context = context.derive('ifjump check')
                jump_context.replacements['$OFFSET'] = str(jump_offset)
                
                return self._parse_state_action(jump, jump_context)
                
            if_ctx = context.remote_derive('ifjump body', 3)
            
            for a in s_yes:
                self._parse_state(actor, if_ctx, ifs, a, func)

            if s_no:
                elses = ZDBlock(actor)
            
                for a in s_no:
                    self._parse_state(actor, if_ctx, elses, a, func)

                ifs.set_else(elses)

            add_state(ifs)
            pop_remote()

        elif s[0] == 'whilejump':
            break_ctx = context.remote_derive('whilejump', 4)
            jump, s_yes, s_no = s[1]
        
            @ZDWhileJumpStatement.generate(actor)
            def whs(jump_offset):
                jump_context = break_ctx.derive('whilejump check')
                jump_context.replacements['$OFFSET'] = str(jump_offset)
                
                return self._parse_state_action(jump, jump_context)

            for a in s_yes:
                loop_ctx = break_ctx.derive('body')
                self._parse_state(actor, loop_ctx, whs, self._mutate_iter_state(a, break_ctx, loop_ctx), func)

            if s_no is not None:
                elses = ZDBlock(actor)
            
                for a in s_no:
                    self._parse_state(actor, context, elses, a, func)

                whs.set_else(elses)
   
            add_state(whs)
            clear_remotes(break_ctx)

        elif s[0] == 'while':
            break_ctx = context.remote_derive('while', 4 if s[1][2] else 3)
            whs = ZDWhileStatement(actor, self._parse_expression(s[1][0], break_ctx), [])
                        
            for a in s[1][1]:
                loop_ctx = break_ctx.derive('body')
                self._parse_state(actor, loop_ctx, whs, self._mutate_iter_state(a, break_ctx, loop_ctx), func)
                
            if s[1][2]:
                elses = ZDBlock(actor)

                for a in s[1][2]:
                    self._parse_state(actor, if_ctx, elses, a, func)

                whs.set_else(elses)

            add_state(whs)
            clear_remotes(break_ctx)
            
        elif s[0] == 'for':
            itername, iteridx, itermode, f_body, f_else = s[1]
            
            if itermode[0] == 'group':
                group_name = context.resolve(itermode[1], 'a parametrized group name')
                
                if group_name.upper() not in self.groups:
                    raise CompilerError("No such group {} to 3 in a for loop in {}!".format(repr(group_name), context.describe()))
                    
                elif self.groups[group_name.upper()]:
                    break_ctx = context.derive('for')
                
                    for i, item in enumerate(self.groups[group_name.upper()]):
                        iter_ctx = break_ctx.derive('loop body')
                        iter_ctx.replacements[itername.upper()] = item
                        
                        if iteridx:
                            iter_ctx.replacements[iteridx.upper()] = str(i)
                        
                        break_skip_size = len(f_body) * (len(self.groups[group_name.upper()]) - i)
                        continue_skip_size = len(f_body) * (len(self.groups[group_name.upper()]) - i)
                        
                        for si, a in enumerate(f_body):
                            self._parse_state(actor, iter_ctx, label, self._mutate_iter_state(a, break_ctx, iter_ctx), label)
                            
                else:
                    else_ctx = context.derive('for-else')
                
                    for a in f_else:
                       self._parse_state(actor, else_ctx, label, a, label)
                       
            else:
                raise CompilerError("Unknown internal for loop iteration mode '{}' in {}! Please report this issue to the author.".format(itermode[0], context.describe()))

        elif s[0] == 'inject':
            r_from, r_name, r_args = s[1]
            r_name = context.resolve(r_name, 'a parametrized macro injection')
             
            if r_from:
                r_from = unstringify(context.resolve(r_from, 'a parametrized extern macro classname'))
            
                if r_from.upper() in self.actor_names:
                    act = self.actor_names[r_from.upper()]
                
                else:
                    raise CompilerError("Unknown extern macro classname {} in {}!".format(repr(r_from), context.describe()))
            
                macros = dict(act.context.macros)
                
            else:
                macros = dict(context.macros)

            if r_name.upper() in macros:            
                if r_from:
                    new_context = context.derive("macro '{}' from {}".format(r_name, act.name))
                    new_context.update(act.context)
                    
                else:
                    new_context = context.derive("macro '{}'".format(r_name))

                (m_args, m_body) = macros[r_name.upper()]

                for rn, an in zip(r_args, m_args):
                    new_context.replacements[an.upper()] = self._parse_argument(rn, context, an)

                for a in m_body:
                    self._parse_state(actor, new_context, label, self._mutate_macro_state(a, new_context), label)

            else:
                if r_from:
                    raise CompilerError("Unknown macro {}.{} in {}!".format(r_from, r_name, context.describe()))
                
                else:
                    raise CompilerError("Unknown macro {} in {}!".format(r_name, context.describe()))

    def _parse_inherit(self, inh, context):
        if inh is None:
            return None

        ptype, pval = inh

        if ptype == 'classname':
            return context.replacements.get(pval.upper(), pval)

        elif ptype == 'template derivation':
            with context.desc_block('template derivation inheritance'):
                return self._parse_template_derivation(pval, context, stringify=False).name

    def _parse_anonym_class(self, anonym_class, context):
        a = dict(anonym_class)
        new_context = context.derive('anonymous class')
        
        classname = '_AnonymClass_{}_{}'.format(self.id, len(self.anonymous_classes))
        
        if a['group']:
            g = unstringify(a['group'])
            
            if g.upper() in self.groups:
                self.groups[g.upper()].append(stringify(classname))
                
            else:
                raise CompilerError("Group '{}' not found while compiling anonymous class in {}!".format(g, context.describe()))
        
        anonym_actor = ZDActor(self, classname, inherit=self._parse_inherit(a['inheritance'], context), context=new_context)

        self._parse_class_body(anonym_actor, anonym_actor.get_context(), a['body'])
        
        context.add_actor(anonym_actor)

        self.anonymous_classes.append(anonym_actor)
        self.inventories.append(anonym_actor)

        return stringify(anonym_actor.name)

    def _derive_class_from_template(self, template, param_values, context, labels=(), macros=(), arrays=(), body=(), name=None, pending=None):
        labels = dict(labels)
        macros = dict(macros)
        arrays = dict(arrays)
        body  = list(body)

        name = name or template.generated_class_name(param_values, make_id(40))

        new_context = context.derive('derivation of template {}'.format(template.name))            
        new_context.replacements.update(template.get_init_replacements(self, context, param_values))
        new_context.replacements['SELF'] = '"' + repr(name)[1:-1] + '"'

        needs_init, actor = template.generate_init_class(self, new_context, param_values, {l.upper() for l in labels.keys()}, {m['name'].upper(): m['args'] for m in macros.values()}, {a['name'].upper(): len(a['value']) for a in arrays.values()}, name=name)
        new_context = actor.get_context()

        if needs_init:
            def pending_oper_gen():
                act = actor
                new_ctx = new_context
                temp = template

                @pending_task(0)
                def pending_oper():                    
                    for btype, bdata in body:
                        if btype == 'array':
                            try:
                                absarray = template.abstract_array_names[bdata['name'].upper()]

                            except KeyError:
                                raise CompilerError("Tried to define an array {} in {} that is not abstractly declared in the template {}!".format(repr(bdata['name']), new_ctx.describe(), repr(template.name)))

                            act.uservars.append({'name': bdata['name'], 'size': len(bdata['value'][1]), 'value': ('arr', bdata['value'][1]), 'type': absarray['type']})
                    
                    self._parse_class_body(act, new_ctx, body)
                    self._parse_class_body(act, new_ctx, temp.parse_data)

                return pending_oper

            if pending:
                pending.put_nowait(pending_oper_gen())

            else:
                pending_oper_gen().func()

            self.actors.append(actor)
            self.actor_names[actor.name.upper()] = actor

        return actor

    def _parse_class_body(self, actor, context, body):
        assert context is actor.context
    
        for btype, bdata in body:
            if btype == 'macro':
                context.macros[bdata['name'].upper()] = (bdata['args'], bdata['body'])

        for btype, bdata in body:
            if btype == 'property':
                ZDProperty(actor, bdata['name'], ', '.join(self._parse_parameter(x, context) for x in bdata['value']))

            elif btype == 'flag':
                actor.flags.add(bdata)

            elif btype == 'flag combo':
                actor.raw.append(bdata)

            elif btype == 'user var':
                bdata = { **bdata, 'value': self._parse_expression(bdata['value'], context) }
                actor.uservars.append(bdata)

            elif btype == 'unflag':
                actor.antiflags.add(bdata)

            elif btype == 'label':
                label = ZDLabel(actor, bdata['name'])

                with context.desc_block("label '{}'".format(label.name)):
                    for s in bdata['body']:
                        self._parse_state(actor, context, label, s, None)

            elif btype == 'function':
                func = ZDFunction(self, actor, bdata['name'])

                with context.desc_block("function '{}'".format(func.name)):
                    for s in bdata['body']:
                        self._parse_state(actor, context, func, s, func)

    def _parse(self, actors):
        calls = []
        parsed_actors = []
        
        context = ZDCodeParseContext(calls=[calls], actors=[parsed_actors])

        actors = list(actors)

        for class_type, a in actors:
            if class_type == 'group':
                gname = a['name'].upper()
                
                if gname in self.groups:
                    self.groups[gname].extend(list(a['items']))
                    
                else:
                    self.groups[gname] = list(a['items'])
                
            elif class_type == 'macro':
                context.macros[a['name']] = (a['args'], a['body'])

        for class_type, a in actors:
            if class_type == 'class template':
                abstract_labels = set()
                abstract_macros = {}
                abstract_arrays = {}
                
                if a['group']:
                    g = unstringify(a['group'])
                
                    if g.upper() not in self.groups:
                        raise CompilerError("Group '{}' not found while compiling template class {}!".format(g, a['classname']))
                        
                    g = g.upper()
                    
                else:
                    g = None

                for btype, bdata in a['body']:
                    if btype == 'abstract label':
                        abstract_labels.add(bdata.upper())

                    elif btype == 'abstract macro':
                        abstract_macros[bdata['name'].upper()] = bdata['args']

                    elif btype == 'abstract array':
                        abstract_arrays[bdata['name'].upper()] = bdata

                template = ZDClassTemplate(a['parameters'], a['body'], abstract_labels, abstract_macros, abstract_arrays, g, self, a['classname'], self._parse_inherit(a['inheritance'], context), a['replacement'], a['class number'])
                context.templates[a['classname']] = template

        pending = queue.PriorityQueue()

        for class_type, a in actors:
            if class_type == 'class':
                with context.desc_block("class '{}'".format(a['classname'])):
                    actor = ZDActor(self, a['classname'], self._parse_inherit(a['inheritance'], context), a['replacement'], a['class number'], context=context)
                    ctx = actor.get_context()
                    
                    if a['group']:
                        g = a['group']
                        
                        if g.upper() in self.groups:
                            self.groups[g.upper()].append(stringify(a['classname']))
                            
                        else:
                            raise CompilerError("Group '{}' not found while compiling class '{}'!".format(g, a['classname']))

                    def pending_oper_gen():
                        actor_ = actor
                        ctx_ = ctx
                        body_ = a['body']

                        @pending_task(2)
                        def pending_oper():
                            self._parse_class_body(actor_, ctx_, body_)

                        return pending_oper

                    pending.put_nowait(pending_oper_gen())

                    self.actors.append(actor)
                    self.actor_names[actor.name.upper()] = actor
                    parsed_actors.append(actor)

            elif class_type == 'static template derivation':
                new_name = a['classname']
                gname = a['group']
                context = context.derive('static template derivation \'{}\''.format(new_name))

                parsed_actors.append(self._parse_template_derivation(a['source'][1], context, pending=pending, name=new_name, stringify=False))
                
                if gname:
                    @pending_task(1)
                    def pending_oper():
                        g = unstringify(gname)
                        
                        if g.upper() not in self.groups:
                            raise CompilerError("No such group {} to add the derivation {} to!".format(repr(g), new_name))
                        
                        self.groups[g.upper()].append(new_name)
                
                    pending.put_nowait(pending_oper)

        while not pending.empty():
            pending.get_nowait().func()

        for c in calls:
            c.post_load()

        for a in parsed_actors:
            a.prepare_spawn_label()

    def __init__(self):
        self.inventories = []
        self.anonymous_classes = []
        self.actors = []
        self.actor_names = {}
        self.groups = {}
        self.id = make_id(35)
        self.calls = set()
        self.num_anonym_macros = 0

    def __decorate__(self):
        if not self.inventories:
            return "\n\n\n".join(decorate(a) for a in self.actors)

        return "\n\n\n".join(["\n".join(
            decorate(i) for i in self.inventories
        )] + [
            decorate(a) for a in self.actors
        ]) # lines split for debugging

    def decorate(self):
        return decorate(self)

