import pygame


# спинбокс для начального окна
class spinBox:
    def __init__(self, position, min=0, max=100, step=1):
        self.rect = pygame.Rect(position, (60, 40))
        self.image = pygame.Surface(self.rect.size)
        self.image.set_alpha(128)

        self.font = pygame.font.Font(None, 36)
        self.buttonRects = [pygame.Rect(35, 5, 20, 10),
                            pygame.Rect(35, 25, 20, 10)]

        self.state = 0
        self.step = step
        self.min = min
        self.max = max

    def draw(self, surface):
        # Draw SpinBox onto surface
        textline = self.font.render(str(self.state), True, (255, 255, 255))

        self.image.fill((102, 179, 255))
        # self.image.convert_alpha()

        # increment button
        pygame.draw.rect(self.image, (255, 255, 255), self.buttonRects[0])
        pygame.draw.polygon(self.image, (0, 0, 0), [(38, 12), (45, 6), (53, 12)])
        # decrement button
        pygame.draw.rect(self.image, (255, 255, 255), self.buttonRects[1])
        pygame.draw.polygon(self.image, (0, 0, 0), [(38, 28), (45, 34), (53, 28)])

        self.image.blit(textline, (5, (self.rect.height - textline.get_height()) // 2))

        surface.blit(self.image, self.rect)

    def increment(self):
        if self.state < self.max:
            self.state += self.step

    def decrement(self):
        if self.state > self.min:
            self.state -= self.step

    def __call__(self, position):
        # enumerate through all button rects
        for idx, btnR in enumerate(self.buttonRects):
            # create a new pygame rect with absolute screen position
            btnRect = pygame.Rect((btnR.topleft[0] + self.rect.topleft[0],
                                   btnR.topleft[1] + self.rect.topleft[1]), btnR.size)

            if btnRect.collidepoint(position):
                if idx == 0:
                    self.increment()
                else:
                    self.decrement()
