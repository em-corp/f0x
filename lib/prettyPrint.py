__all__ = []

from colorama import Fore as f
from colorama import Back as b
from colorama import Style as s


class Prettify:
    
    def __cont__(t, r, c):
        return t.replace(r, r + c)

    # *** text ***
    def red(text):
        return f.RED + Prettify.__cont__(text, f.RESET, f.RED) + f.RESET
    
    def black(text):
        return f.BLACK + Prettify.__cont__(text, f.RESET, f.BLACK) + f.RESET

    def blue(text):
        return f.BLUE + Prettify.__cont__(text, f.RESET, f.BLUE) + f.RESET

    def cyan(text):
        return f.CYAN + Prettify.__cont__(text, f.RESET, f.CYAN) + f.RESET

    def green(text):
        return f.GREEN + Prettify.__cont__(text, f.RESET, f.GREEN) + f.RESET

    def magenta(text):
        return f.MAGENTA + Prettify.__cont__(text, f.RESET, f.MAGENTA) + f.RESET

    def white(text):
        return f.WHITE + Prettify.__cont__(text, f.RESET, f.WHITE) + f.RESET

    def yellow(text):
        return f.YELLOW + Prettify.__cont__(text, f.RESET, f.YELLOW) + f.RESET

    def light_black(text):
        return f.LIGHTBLACK_EX + Prettify.__cont__(text, f.RESET, 
                                                   f.LIGHTBLACK_EX) + f.RESET

    def light_blue(text):
        return f.LIGHTBLUE_EX + Prettify.__cont__(text, f.RESET, 
                                                  f.LIGHTBLUE_EX) + f.RESET

    def light_cyan(text):
        return f.LIGHTCYAN_EX + Prettify.__cont__(text, f.RESET, 
                                                  f.LIGHTCYAN_EX) + f.RESET
    
    def light_green(text):
        return f.LIGHTGREEN_EX + Prettify.__cont__(text, f.RESET, 
                                                   f.LIGHTGREEN_EX) + f.RESET

    def light_magenta(text):
        return f.LIGHTMAGENTA_EX + Prettify.__cont__(text, f.RESET, 
                                                     f.LIGHTMAGENTA_EX) + \
                                                     f.RESET

    def light_red(text):
        return f.LIGHTRED_EX + Prettify.__cont__(text, f.RESET, 
                                                 f.LIGHTRED_EX) + f.RESET

    def light_white(text):
        return f.LIGHTWHITE_EX + Prettify.__cont__(text, f.RESET, 
                                                   f.LIGHTWHITE_EX) + f.RESET

    def light_yellow(text):
        return f.LIGHTYELLOW_EX + Prettify.__cont__(text, f.RESET, 
                                                    f.LIGHTYELLOW_EX) + f.RESET
    
    # *** background ***
    def on_red(text):
        return b.RED + Prettify.__cont__(text, b.RESET, b.RED) + b.RESET
    
    def on_black(text):
        return b.BLACK + Prettify.__cont__(text, b.RESET, b.BLACK) + b.RESET

    def on_blue(text):
        return b.BLUE + Prettify.__cont__(text, b.RESET, b.BLUE) + b.RESET

    def on_cyan(text):
        return b.CYAN + Prettify.__cont__(text, b.RESET, b.CYAN) + b.RESET

    def on_green(text):
        return b.GREEN + Prettify.__cont__(text, b.RESET, b.GREEN) + b.RESET

    def on_magenta(text):
        return b.MAGENTA + Prettify.__cont__(text, b.RESET, b.MAGENTA) + b.RESET

    def on_white(text):
        return b.WHITE + Prettify.__cont__(text, b.RESET, b.WHITE) + b.RESET

    def on_yellow(text):
        return b.YELLOW + Prettify.__cont__(text, b.RESET, b.YELLOW) + b.RESET

    def on_light_black(text):
        return b.LIGHTBLACK_EX + Prettify.__cont__(text, b.RESET, 
                                                   b.LIGHTBLACK_EX) + b.RESET

    def on_light_blue(text):
        return b.LIGHTBLUE_EX + Prettify.__cont__(text, b.RESET, 
                                                  b.LIGHTBLUE_EX) + b.RESET

    def on_light_cyan(text):
        return b.LIGHTCYAN_EX + Prettify.__cont__(text, b.RESET, 
                                                  b.LIGHTCYAN_EX) + b.RESET
    
    def on_light_green(text):
        return b.LIGHTGREEN_EX + Prettify.__cont__(text, b.RESET, 
                                                   b.LIGHTGREEN_EX) + b.RESET

    def on_light_magenta(text):
        return b.LIGHTMAGENTA_EX + Prettify.__cont__(text, b.RESET, 
                                                     b.LIGHTMAGENTA_EX) + \
                                                     b.RESET

    def on_light_red(text):
        return b.LIGHTRED_EX + Prettify.__cont__(text, b.RESET, 
                                                 b.LIGHTRED_EX) + b.RESET

    def on_light_white(text):
        return b.LIGHTWHITE_EX + Prettify.__cont__(text, b.RESET, 
                                                   b.LIGHTWHITE_EX) + b.RESET

    def on_light_yellow(text):
        return b.LIGHTYELLOW_EX + Prettify.__cont__(text, b.RESET, 
                                                    b.LIGHTYELLOW_EX) + b.RESET

    # *** sytle ***

    def as_bold(text):
        return s.BRIGHT + Prettify.__cont__(text, s.RESET_ALL, 
                                            s.BRIGHT) + s.RESET_ALL

    def as_dim(text):
        return s.DIM + Prettify.__cont__(text, s.RESET_ALL, 
                                         s.BRIGHT) + s.RESET_ALL

    def as_normal(text):
        return s.NORMAL + Prettify.__cont__(text, s.RESET_ALL, 
                                            s.BRIGHT) + s.RESET_ALL

    # *** logger ***
    def p_error(text):
        print("[{}]: {}".format(Prettify.as_bold(Prettify.red('ERROR')), text))

    def p_info(text):
        print("[{}]: {}".format(Prettify.cyan('INFO'), text))

    def p_warn(text):
        print("[{}]: {}".format(Prettify.red('WARN'), text))
    
    def p_debug(text):
        print("[{}]: {}".format(Prettify.as_bold(Prettify.yellow('DEBUG')),
            text))

    def p_log(text, header='*'):
        print("[{}]: {}".format(Prettify.as_bold(Prettify.blue(header)), text))

    def p_clog(text, header):
        print("[{}]: {}".format(header, text))
