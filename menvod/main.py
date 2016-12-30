import sys
sys.path.append('../modules')
import gl_main
import stateSystem
#import yaml
import mega
import ByteFont
import lists
import datetime

data_dir = 'data/'
#TODO make test and write TZ and clean up it
#### DEVELOP AREA START #### (future to refactor)
def build_status_str():
    s = "{time}"
    time = datetime.datetime.now()
    time = "{}:{}".format(time.hour, time.minute)
    params = {'time': time,
            }
    return s.format(**params)

def render_status():
    ByteFont.draw_text(build_status_str(), y=0, x=0, color=(1, 1, 1))

#### DEVELOP AREA END ####
def std_keypress(key_sym, world=None):
    keyboard_fun = {
            'H':lambda x, y: x,
            'j':lambda x, y: lists.next(),
            }
    keyboard_fun.get(key_sym, lambda x, y: x)(key_sym, world)

def std_draw(render_data):
    render_status()
    lists.render()

####
def init():
    stateSystem.addState('std')
    stateSystem.changeState('std')
    stateSystem.setEventHandler('std', 'keypress', std_keypress)
    stateSystem.setEventHandler('std', 'draw', std_draw)
    font = ByteFont.init_font(data_dir + ByteFont.font_file, 10, 16)
    font10x16 = ByteFont.init_font(data_dir + ByteFont.font_file10x16, 10, 16)
    ByteFont.set_fonts(font, font10x16)
    lists.init(2, 4, 'ab', 'cd', '3.21')

def DrawGLScene():
    gl_main.gl_draw_pre()
    stateSystem.handleEvent('draw', None)
    gl_main.gl_error_msg()

def keyPressed(*args):
    if args[0] == gl_main.ESCAPE:
        sys.exit()
    if ord(args[0]) > 127:
        print('Switch to Latin keyboard layout. Переключите на латинскую раскладку.')
        return
    key_sym = bytes.decode(args[0])
    #print(key_sym, ord(args[0]))
    stateSystem.handleEvent('keypress', key_sym, None)
    DrawGLScene()

def main():
    gl_main.gl_main(name='menvod', draw_func=DrawGLScene, key_func=keyPressed)
    init()
    gl_main.gl_start()

if __name__=='__main__':
    main() 
