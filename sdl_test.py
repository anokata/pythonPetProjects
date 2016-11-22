import sys
import sdl2.ext

def run():
    resources = sdl2.ext.Resources(__file__, "platformer")
    sdl2.ext.init()
    window = sdl2.ext.Window("SRG", size=(200, 200))
    window.show()
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sprite = factory.from_image(resources.get_path("sky0.png"))
    s2 = sprite.subsprite((2, 2, 10, 10))

    s2r = sdl2.ext.Renderer(s2)
    tfactory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=s2r)
    texture = tfactory.from_image(resources.get_path("sky0.png"))
    
    #s2r.copy(texture)

    spriterenderer = factory.create_sprite_render_system(window)

    running = True
    i = 1000
    fps = 0
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == 27:
                    running = False
                    break
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    print(key, sdl2.SDLK_q)
        i -= 1
        if i == 0:
            i = 1000 
            x, y = sprite.position
            sdl2.ext.fill(spriterenderer.surface, sdl2.ext.Color(0, 0, 0))
            sprite.position = x+1, y+1
            spriterenderer.render([sprite, s2])
        window.refresh()
    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
