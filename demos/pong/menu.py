from pgpu import *


class Menu(Component):
    def init(self):
        self.title_font = pygame.Font(None, 150)
        self.button_font = pygame.Font(None, 80)
        self.title_txt = graphics.font_texture(self.title_font, "PONG", True, "white")
        self.play_txt = graphics.font_texture(self.button_font, "PLAY", True, "white")
        self.title_rect = self.title_txt.get_rect(
            center=Camera.project_point((0, -Window.bounds.h // 4))
        )
        self.play_rect = self.play_txt.get_rect(center=Camera.project_point((0, 0)))

    def render(self):
        self.title_txt.draw(dstrect=self.title_rect)
        self.play_txt.draw(dstrect=self.play_rect)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.play_rect.collidepoint(event.pos):
                    Scenes.call_scene_func("main_scene")


class MenuEntity(Entity):
    start_components = [Menu]

    @classmethod
    def instantiate(cls):
        menu = MenuEntity(Transform(), ["updates", "rendering", "event-handler"], None)
        return menu
