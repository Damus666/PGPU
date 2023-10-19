from pgpu import *


class Ball(Component):
    unique = True

    def init(self):
        self.manager: Manager = self.scene.ManagerEntity.Manager
        self.speed = 500
        self.direction = vector(random.choice([-1, 1]), random.choice([-1, 1]))
        self.radius = self.entity.texture.width // 2
        self.player: PlatformEntity = None
        self.enemy: PlatformEntity = None

    def update(self):
        if not self.manager.can_update:
            return
        self.transform.position += self.direction * self.speed * Time.delta_time
        if self.transform.position.y + self.radius > Window.bounds.h // 2:
            self.transform.position.y = Window.bounds.h // 2 - self.radius
            self.direction.y *= -1
        if self.transform.position.y - self.radius < -Window.bounds.h // 2:
            self.transform.position.y = -Window.bounds.h // 2 + self.radius
            self.direction.y *= -1
        if self.entity.box.colliderect(self.player.box):
            self.transform.position.x = self.player.box.right + self.radius
            self.direction.x *= -1
        if self.entity.box.colliderect(self.enemy.box):
            self.transform.position.x = self.enemy.box.left - self.radius
            self.direction.x *= -1
        if self.transform.position.x - self.radius < -Window.bounds.w // 2:
            self.transform.position = vector()
            self.manager.enemy_score()
            self.direction = vector(random.choice([-1, 1]), random.choice([-1, 1]))
        if self.transform.position.x + self.radius > Window.bounds.w // 2:
            self.transform.position = vector()
            self.manager.player_score()
            self.direction = vector(random.choice([-1, 1]), random.choice([-1, 1]))


class Platform(Component):
    unique = True
    speed = 350
    enemy_speed = 300

    def init(self):
        self.ball: BallEntity = self.scene.BallEntity
        self.manager: Manager = self.scene.ManagerEntity.Manager
        self.direction = 0

    def update(self):
        if not self.manager.can_update:
            return
        self.player_update() if self.isplayer else self.enemy_update()

    def player_update(self):
        self.transform.position.y += (
            Input.get_axis("vertical") * Time.delta_time * self.speed
        )
        if (
            self.transform.position.y
            < -Window.bounds.h // 2 + self.entity.texture.height // 2
        ):
            self.transform.position.y = (
                -Window.bounds.h // 2 + self.entity.texture.height // 2
            )
        if (
            self.transform.position.y
            > Window.bounds.h // 2 - self.entity.texture.height // 2
        ):
            self.transform.position.y = (
                Window.bounds.h // 2 - self.entity.texture.height // 2
            )

    def enemy_update(self):
        if self.ball.transform.position.x > 0 and self.ball.Ball.direction.x > 0:
            self.direction = -mathf.signof(
                self.transform.position.y - self.ball.transform.position.y
            )
            self.transform.position.y += (
                self.direction * self.enemy_speed * Time.delta_time
            )


class PlatformEntity(Entity):
    start_components = [Platform]

    @classmethod
    def instantiate(cls, tag, isplayer):
        platform = PlatformEntity(
            Transform(),
            ["visible-main", "updates"],
            graphics.box_texture((20, Window.bounds.h // 5), "white"),
            [tag],
        )
        platform.Platform.isplayer = isplayer
        if isplayer:
            platform.transform.position.x = -Window.bounds.w // 2 + 15
        else:
            platform.transform.position.x = Window.bounds.w // 2 - 15
        if isplayer:
            Scenes.scene.BallEntity.Ball.player = platform
        else:
            Scenes.scene.BallEntity.Ball.enemy = platform
        return platform


class BallEntity(Entity):
    start_components = [Ball]
    unique = True

    @classmethod
    def instantiate(cls):
        return BallEntity(
            Transform(),
            ["visible-main", "updates"],
            graphics.circle_texture(20, "white"),
            ["ball"],
        )


class Manager(Component):
    unique = True

    def init(self):
        self.line_rect = pygame.Rect(0, 0, 10, Window.bounds.h)
        self.line_rect.center = (0, 0)
        self.white = pygame.Color("white")
        self.can_update = False
        self.scores = {
            "player": 0,
            "enemy": 0,
        }
        self.font = pygame.Font(None, 80)
        Time.add_timer("restart", 3000, self.finish_restart, False)
        self.gen_scores()
        self.restart_game()

    def finish_restart(self):
        self.can_update = True
        Time.deactivate_timer("restart")

    def restart_game(self):
        Time.activate_timer("restart")
        self.can_update = False

    def player_score(self):
        self.scores["player"] += 1
        self.after_score()

    def enemy_score(self):
        self.scores["enemy"] += 1
        self.after_score()

    def after_score(self):
        self.gen_scores()
        self.restart_game()

    def gen_scores(self):
        self.p_score_txt = graphics.font_texture(
            self.font, f"{self.scores['player']}", True, "white"
        )

        self.e_score_txt = graphics.font_texture(
            self.font, f"{self.scores['enemy']}", True, "white"
        )

        self.p_score_rect = self.p_score_txt.get_rect(
            midright=Camera.project_point((-self.p_score_txt.width, 0))
        )
        self.e_score_rect = self.e_score_txt.get_rect(
            midleft=Camera.project_point((self.e_score_txt.width, 0))
        )

    def render(self):
        render.project_filled_rect(self.line_rect, self.white)
        self.p_score_txt.draw(dstrect=self.p_score_rect)
        self.e_score_txt.draw(dstrect=self.e_score_rect)
        if not self.can_update:
            self.time_txt.draw(dstrect=self.time_rect)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Scenes.call_scene_func("menu_scene")

    def update(self):
        if not self.can_update:
            time_left = Time.get_timer("restart").time_left()
            time_left = int(time_left * 0.001) + 1
            self.time_txt = graphics.font_texture(
                self.font, f"{time_left}", True, "white", (30, 30, 30)
            )
            self.time_rect = self.time_txt.get_rect(
                center=Camera.project_point((0, -Window.bounds.h // 4))
            )
        Window.window.title = f"{Time.framerate:.0f} FPS"


class ManagerEntity(Entity):
    start_components = [Manager]
    unique = True

    @classmethod
    def instantiate(cls):
        return ManagerEntity(
            Transform(), ["updates", "rendering", "event-handler"], None
        )
