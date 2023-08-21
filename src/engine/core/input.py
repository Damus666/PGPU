import pygame
from ..utils import _pygame_key_codes
from .time import Time
from ..extension.math import Math

class InputAxis:
    def __init__(self, p, n, ap, an, el):
        self.pos = p
        self.neg = n
        self.alt_p = ap
        self.alt_n = an
        self.elasticity = el
        self.value = 0

    def _update(self):
        any_press = False
        if (self.pos and Input.keys_pressed[self.pos]) or (self.alt_p and Input.keys_pressed[self.alt_p]):
            self.value += self.elasticity*Time.delta_time
            if self.value > 1: self.value = 1
            any_press = True
        if (self.neg and Input.keys_pressed[self.neg]) or (self.alt_n and Input.keys_pressed[self.alt_n]):
            self.value -= self.elasticity*Time.delta_time
            if self.value < -1: self.value = -1
            any_press = True
        if not any_press:
            if self.value != 0:
                old = Math.signof(self.value)
                self.value -= self.elasticity*old*Time.delta_time
                if old != Math.signof(self.value): self.value = 0


class Input:
    frame_events:list[pygame.event.Event] = []
    keys_pressed:list[bool] = []
    keyboard_focused:bool = True
    buttons_pressed:list[bool] = []
    mouse_position:pygame.Vector2 = pygame.Vector2()
    mouse_relative:pygame.Vector2 = pygame.Vector2()
    mouse_wheel:pygame.Vector2 = pygame.Vector2()
    mouse_visible:bool = True
    mouse_focused:bool = True
    any_key: bool = False
    any_mouse: bool = False
    _axis:dict[str,InputAxis] = {}
    _key_data:dict[int,int] = dict()
    _mouse_data:dict[int,int] = dict()
    _actions:dict[str,list[int]] = dict()
    default_elasticity: float = 1

    @classmethod
    def _init(cls, default_elasticity):
        cls.default_elasticity = default_elasticity
        for kc in _pygame_key_codes: cls._key_data[kc] = 0
        for i in range(30): cls._mouse_data[i] = 0
        cls.add_axis("horizontal",KeyCode.right,KeyCode.left,KeyCode.d,KeyCode.a)
        cls.add_axis("vertical",KeyCode.down,KeyCode.up,KeyCode.s,KeyCode.w)
        cls.add_action("jump",KeyCode.space)
        cls._update([])

    @classmethod
    def _update(cls, events):
        cls.frame_events = events
        cls.any_key = False
        cls.any_mouse = False
        cls.keys_pressed = pygame.key.get_pressed()
        cls.keyboard_focused = pygame.key.get_focused()
        cls.buttons_pressed = pygame.mouse.get_pressed()
        cls.mouse_position = pygame.mouse.get_pos()
        cls.mouse_relative = pygame.mouse.get_rel()
        cls.mouse_visible = pygame.mouse.get_visible()
        cls.mouse_focused = pygame.mouse.get_focused()
        cls._key_data = dict.fromkeys(cls._key_data,0)
        cls._mouse_data = dict.fromkeys(cls._mouse_data,0)
        for axis in cls._axis.values(): axis._update()

    @classmethod
    def _event(cls, event):
        if event.type == pygame.KEYDOWN:
            cls.any_key = True
            cls._key_data[event.key] = 1
        elif event.type == pygame.KEYUP: cls._key_data[event.key] = 2
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cls.any_mouse = True
            cls._mouse_data[event.button] = 1
        elif event.type == pygame.MOUSEBUTTONUP: cls._mouse_data[event.button] = 2
        elif event.type == pygame.MOUSEWHEEL:
            cls.mouse_wheel.y = event.y
            cls.mouse_wheel.x = event.x

    @classmethod
    def add_action(cls, name:str, *keys):
        if name in cls._actions: return
        cls._actions[name] = keys

    @classmethod
    def add_axis(cls, name:str, positive_key:int=None, negative_key:int=None, alt_positive:int=None, alt_negative:int=None, elasticity:float=None):
        if name in cls._axis: return
        if elasticity is None: elasticity = cls.default_elasticity
        cls._axis[name] = InputAxis(positive_key,negative_key,alt_positive,alt_negative,elasticity)

    @classmethod
    def get_axis(cls, name:str)->float:
        return cls._axis[name].value
    
    @classmethod
    def set_mouse_visibility(cls, visible:bool):
        pygame.mouse.set_visible(visible)
        cls.mouse_visible = visible

    @classmethod
    def set_mouse_position(cls, position):
        pygame.mouse.set_pos(position)
        cls.mouse_position = pygame.Vector2(position)

    @staticmethod
    def key_from_name(name:str)->int:
        return pygame.key.key_code(name)
    
    @staticmethod
    def name_from_key(key_code:int)->str:
        return pygame.key.name(key_code)
    
    @classmethod
    def get_key(cls,key_code:int)->bool:
        return cls.keys_pressed[key_code]
    
    @classmethod
    def get_key_down(cls,key_code:int)->bool:
        return cls._key_data[key_code] == 1
    
    @classmethod
    def get_key_up(cls,key_code:int)->bool:
        return cls._key_data[key_code] == 2
    
    @classmethod
    def get_mouse(cls,button:int)->bool:
        return cls.buttons_pressed[button]
    
    @classmethod
    def get_mouse_down(cls,button:int)->bool:
        return cls._mouse_data[button+1] == 1
    
    @classmethod
    def get_mouse_up(cls,button:int)->bool:
        return cls._mouse_data[button+1] == 2
    
    @classmethod
    def get_action(cls, name:str)->bool:
        for key_code in cls._actions[name]:
            if cls.keys_pressed[key_code]: return True
        return False
    
    @classmethod
    def get_action_down(cls, name:str)->bool:
        for key_code in cls._actions[name]:
            if cls._key_data[key_code] == 1: return True
        return False
    
    @classmethod
    def get_action_up(cls, name:str)->bool:
        for key_code in cls._actions[name]:
            if cls._key_data[key_code] == 2: return True
        return False


class KeyCode:
    backspace =  pygame.K_BACKSPACE
    return_ =  pygame.K_RETURN
    tab =  pygame.K_TAB
    escape =  pygame.K_ESCAPE
    space =  pygame.K_SPACE
    comma =  pygame.K_COMMA
    minus =  pygame.K_MINUS
    period =  pygame.K_PERIOD
    slash =  pygame.K_SLASH
    alpha0 =  pygame.K_0
    alpha1 =  pygame.K_1
    alpha2 =  pygame.K_2
    alpha3 =  pygame.K_3
    alpha4 =  pygame.K_4
    alpha5 =  pygame.K_5
    alpha6 =  pygame.K_6
    alpha7 =  pygame.K_7
    alpha8 =  pygame.K_8
    alpha9 =  pygame.K_9
    semicolon =  pygame.K_SEMICOLON
    equals =  pygame.K_EQUALS
    leftbracket =  pygame.K_LEFTBRACKET
    rightbracket =  pygame.K_RIGHTBRACKET
    backslash =  pygame.K_BACKSLASH
    backquote =  pygame.K_BACKQUOTE
    a =  pygame.K_a
    b =  pygame.K_b
    c =  pygame.K_c
    d =  pygame.K_d
    e =  pygame.K_e
    f =  pygame.K_f
    g =  pygame.K_g
    h =  pygame.K_h
    i =  pygame.K_i
    j =  pygame.K_j
    K =  pygame.K_k
    l =  pygame.K_l
    m =  pygame.K_m
    n =  pygame.K_n
    o =  pygame.K_o
    p =  pygame.K_p
    q =  pygame.K_q
    r =  pygame.K_r
    s =  pygame.K_s
    t =  pygame.K_t
    u =  pygame.K_u
    v =  pygame.K_v
    w =  pygame.K_w
    x =  pygame.K_x
    y =  pygame.K_y
    z =  pygame.K_z
    delete =  pygame.K_DELETE
    KP0 =  pygame.K_KP0
    KP1 =  pygame.K_KP1
    KP2 =  pygame.K_KP2
    KP3 =  pygame.K_KP3
    KP4 =  pygame.K_KP4
    KP5 =  pygame.K_KP5
    KP6 =  pygame.K_KP6
    KP7 =  pygame.K_KP7
    KP8 =  pygame.K_KP8
    KP9 =  pygame.K_KP9
    KPperiod =  pygame.K_KP_PERIOD
    KPdivide =  pygame.K_KP_DIVIDE
    KPmultiply =  pygame.K_KP_MULTIPLY
    KPminus =  pygame.K_KP_MINUS
    KPplus =  pygame.K_KP_PLUS
    KPenter =  pygame.K_KP_ENTER
    KPequals =  pygame.K_KP_EQUALS
    up =  pygame.K_UP
    down =  pygame.K_DOWN
    right =  pygame.K_RIGHT
    left =  pygame.K_LEFT
    insert =  pygame.K_INSERT
    home =  pygame.K_HOME
    end =  pygame.K_END
    pageup =  pygame.K_PAGEUP
    pagedown =  pygame.K_PAGEDOWN
    f1 =  pygame.K_F1
    f2 =  pygame.K_F2
    f3 =  pygame.K_F3
    f4 =  pygame.K_F4
    f5 =  pygame.K_F5
    f6 =  pygame.K_F6
    f7 =  pygame.K_F7
    f8 =  pygame.K_F8
    f9 =  pygame.K_F9
    f10 =  pygame.K_F10
    f11 =  pygame.K_F11
    f12 =  pygame.K_F12
    numlock =  pygame.K_NUMLOCK
    capslock =  pygame.K_CAPSLOCK
    rshift =  pygame.K_RSHIFT
    lshift =  pygame.K_LSHIFT
    rctrl =  pygame.K_RCTRL
    lctrl =  pygame.K_LCTRL
    ralt =  pygame.K_RALT
    lalt =  pygame.K_LALT