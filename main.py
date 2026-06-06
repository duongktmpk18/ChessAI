import pygame
import os.path
import random
from copy import deepcopy
from define import *
from pieces import *
from tools import *
from AI import *
from AI_sunfish import AI_Sunfish


class Board():
    def __init__(self, screen):
        self.screen = screen
        self.color = BLUE

    def draw_board(self, C):
        pygame.draw.rect(self.screen, C, (PIECE_SIZE-4, PIECE_SIZE-4, 8*PIECE_SIZE+8, 8*PIECE_SIZE+8), 4)
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    self.color = WHITE
                else:
                    self.color = GREEN
                pygame.draw.rect(
                    self.screen, self.color,
                    (PIECE_SIZE*(x+1), PIECE_SIZE*(y+1), PIECE_SIZE, PIECE_SIZE))


class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.clock = pygame.time.Clock()
        try:
            self.font = pygame.font.Font("Cinzel.ttf", 35)
            self.font2 = pygame.font.Font("Cinzel.ttf", 60)
            self.font3 = pygame.font.Font("PressStart2P.ttf", 16)
        except:
            self.font = pygame.font.SysFont("Arial", 45)
            self.font2 = pygame.font.SysFont("Arial Black", 70)
            self.font3 = pygame.font.SysFont("Arial", 20)
            
        try:
            self.hover_sound = pygame.mixer.Sound('hover.wav')
            self.click_sound = pygame.mixer.Sound('click.wav')
        except:
            self.hover_sound = None
            self.click_sound = None
        # Load generated pixel art background
        try:
            self.bg_image = pygame.image.load("bg.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_SIZE, SCREEN_SIZE))
        except:
            self.bg_image = None
            
        try:
            pygame.mixer.music.load('bgm.ogg')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            pass

    def update_and_draw_background(self):
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((20, 20, 40))

    def run(self):
        while True:
            option = self.Menu()
            if option == -1:
                break
                
            time_control = self.TimeMenu()
            if time_control == -1:
                continue
            
            while True:
                board = Board(self.screen)
                pieces = Pieces(self.screen)
                cmate = -1
                
                if option == 1:
                    cmate = self.Game_player_vs_player(board, pieces, time_control)
                elif option == 2:
                    cmate = self.Game_player_vs_AI_Minimax(board, pieces, time_control)
                
                if cmate == -3:
                    continue
                else:
                    break
            
            if cmate == -2:
                continue
            
            if not self.Game_Over(board, pieces, cmate):
                break
        pygame.quit()

    def ask_exit_confirm(self):
        # Semi-transparent dark overlay
        overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        dialog_width, dialog_height = 320, 140
        dialog_rect = pygame.Rect(SCREEN_SIZE/2 - dialog_width/2, SCREEN_SIZE/2 - dialog_height/2, dialog_width, dialog_height)
        
        # Outer dark border
        pygame.draw.rect(self.screen, (30, 25, 25), dialog_rect, border_radius=8)
        # Inner fill
        pygame.draw.rect(self.screen, (50, 40, 40), dialog_rect.inflate(-4, -4), border_radius=8)
        # Inner gold border
        pygame.draw.rect(self.screen, (200, 150, 80), dialog_rect.inflate(-8, -8), 2, border_radius=8)
        
        font = pygame.font.SysFont("Arial", 18, bold=True)
        text = font.render("Are you sure you want to quit?", True, (255, 230, 150))
        text_rect = text.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 40))
        self.screen.blit(text, text_rect)
        
        btn_yes = pygame.Rect(dialog_rect.centerx - 100, dialog_rect.y + 80, 80, 35)
        btn_no = pygame.Rect(dialog_rect.centerx + 20, dialog_rect.y + 80, 80, 35)
        
        last_hover_yes = False
        last_hover_no = False
        
        while True:
            pos = pygame.mouse.get_pos()
            hover_yes = btn_yes.collidepoint(pos)
            hover_no = btn_no.collidepoint(pos)
            
            if hover_yes and not last_hover_yes:
                if self.hover_sound: self.hover_sound.play()
            if hover_no and not last_hover_no:
                if self.hover_sound: self.hover_sound.play()
            last_hover_yes = hover_yes
            last_hover_no = hover_no

            # Draw YES button
            if hover_yes:
                pygame.draw.rect(self.screen, (255, 200, 50), btn_yes.inflate(6, 6), border_radius=6)
            pygame.draw.rect(self.screen, (160, 40, 40), btn_yes, border_radius=5)
            pygame.draw.rect(self.screen, (100, 20, 20), btn_yes, 2, border_radius=5)
            text_yes = font.render("Yes", True, (255, 255, 255) if hover_yes else (220, 200, 180))
            self.screen.blit(text_yes, text_yes.get_rect(center=btn_yes.center))
            
            # Draw NO button
            if hover_no:
                pygame.draw.rect(self.screen, (255, 200, 50), btn_no.inflate(6, 6), border_radius=6)
            pygame.draw.rect(self.screen, (40, 120, 40), btn_no, border_radius=5)
            pygame.draw.rect(self.screen, (20, 80, 20), btn_no, 2, border_radius=5)
            text_no = font.render("No", True, (255, 255, 255) if hover_no else (220, 200, 180))
            self.screen.blit(text_no, text_no.get_rect(center=btn_no.center))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hover_yes:
                        if self.click_sound: self.click_sound.play()
                        return True
                    if hover_no:
                        if self.click_sound: self.click_sound.play()
                        return False

    def handle_settings_menu(self):
        menu_rect = pygame.Rect(10, 45, 140, 85)
        btn_reset = pygame.Rect(15, 50, 130, 35)
        btn_exit = pygame.Rect(15, 90, 130, 35)
        
        font_small = pygame.font.SysFont("Arial", 15, bold=True)
        
        pygame.draw.rect(self.screen, (30, 25, 25), menu_rect, border_radius=5)
        pygame.draw.rect(self.screen, (50, 40, 40), menu_rect.inflate(-4, -4), border_radius=5)
        pygame.draw.rect(self.screen, (200, 150, 80), menu_rect.inflate(-6, -6), 1, border_radius=5)
        
        last_hover_reset = False
        last_hover_exit = False
        
        while True:
            pos = pygame.mouse.get_pos()
            hover_reset = btn_reset.collidepoint(pos)
            hover_exit = btn_exit.collidepoint(pos)
            
            if hover_reset and not last_hover_reset:
                if self.hover_sound: self.hover_sound.play()
            if hover_exit and not last_hover_exit:
                if self.hover_sound: self.hover_sound.play()
            last_hover_reset = hover_reset
            last_hover_exit = hover_exit
            
            # Draw Reset button
            color_reset = (160, 96, 48) if hover_reset else (100, 70, 40)
            pygame.draw.rect(self.screen, color_reset, btn_reset, border_radius=4)
            pygame.draw.rect(self.screen, (80, 40, 15), btn_reset, 1, border_radius=4)
            text_color = (255, 255, 255) if hover_reset else (220, 200, 180)
            text_reset = font_small.render("Reset Game", True, text_color)
            self.screen.blit(text_reset, text_reset.get_rect(center=btn_reset.center))
            
            # Draw Exit button
            color_exit = (160, 96, 48) if hover_exit else (100, 70, 40)
            pygame.draw.rect(self.screen, color_exit, btn_exit, border_radius=4)
            pygame.draw.rect(self.screen, (80, 40, 15), btn_exit, 1, border_radius=4)
            text_color = (255, 255, 255) if hover_exit else (220, 200, 180)
            text_exit = font_small.render("Exit to Menu", True, text_color)
            self.screen.blit(text_exit, text_exit.get_rect(center=btn_exit.center))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.ask_exit_confirm():
                        return 2
                    return 0
                if event.type == MOUSEBUTTONDOWN:
                    if hover_reset:
                        if self.click_sound: self.click_sound.play()
                        return 1
                    elif hover_exit:
                        if self.click_sound: self.click_sound.play()
                        if self.ask_exit_confirm():
                            return 2
                        
                        # Re-draw the settings menu background once they say NO 
                        # so that it doesn't leave the dialog on screen
                        pygame.draw.rect(self.screen, (30, 25, 25), menu_rect, border_radius=5)
                        pygame.draw.rect(self.screen, (50, 40, 40), menu_rect.inflate(-4, -4), border_radius=5)
                        pygame.draw.rect(self.screen, (200, 150, 80), menu_rect.inflate(-6, -6), 1, border_radius=5)
                        # We must also re-draw the board!
                        # Oh wait, handle_settings_menu blocks the loop. 
                        # If the user says NO, we return 0 and the main loop re-draws everything.
                        return 0
                    else:
                        # Click outside menu
                        return 0

    def Menu(self):
        # Menu options with their positions and values
        menu_options = [
            {"text": "PLAYER VS PLAYER", "y_offset": 10, "value": 1},
            {"text": "PLAYER VS AI", "y_offset": 70, "value": 2},
            {"text": "QUIT GAME", "y_offset": 130, "value": -1}
        ]

        option = -1
        running = True
        selected_idx = 0
        last_hovered = -1
        last_mouse_pos = pygame.mouse.get_pos()
        
        while running:
            self.update_and_draw_background()

            # Draw central menu panel
            panel_width, panel_height = 420, 400
            panel_rect = pygame.Rect(SCREEN_SIZE/2 - panel_width/2, 45, panel_width, panel_height)
            
            # Outer dark border
            pygame.draw.rect(self.screen, (30, 25, 25), panel_rect, border_radius=5)
            # Inner semi-transparent fill
            s = pygame.Surface((panel_width-10, panel_height-10))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            self.screen.blit(s, (panel_rect.x+5, panel_rect.y+5))
            # Inner gold border
            pygame.draw.rect(self.screen, (200, 150, 80), panel_rect.inflate(-10, -10), 2, border_radius=5)

            # Draw title with glowing effect
            title_text = "CHESS GAME"
            title_glow = self.font2.render(title_text, True, (100, 70, 20))
            title = self.font2.render(title_text, True, (255, 230, 150))
            
            title_center = (SCREEN_SIZE/2 - title.get_width() // 2, panel_rect.y + 30)
            self.screen.blit(title_glow, (title_center[0]+2, title_center[1]+2))
            self.screen.blit(title, title_center)

            # Mouse  hover effect
            mouse_pos = pygame.mouse.get_pos()
            mouse_moved = (mouse_pos != last_mouse_pos)
            last_mouse_pos = mouse_pos
            
            # Menu options with hover effect
            for idx, opt in enumerate(menu_options):
                y_pos = SCREEN_SIZE/2 + opt["y_offset"]
                btn_width, btn_height = 280, 40
                btn_rect = pygame.Rect(SCREEN_SIZE/2 - btn_width/2, y_pos, btn_width, btn_height)
                
                if mouse_moved and btn_rect.collidepoint(mouse_pos):
                    selected_idx = idx
                
                hover = (idx == selected_idx)
                
                # Draw glowing aura if hovered
                if hover:
                    aura_rect = btn_rect.inflate(8, 8)
                    pygame.draw.rect(self.screen, (255, 200, 50), aura_rect, border_radius=8)
                
                # Draw wooden button
                pygame.draw.rect(self.screen, (160, 96, 48), btn_rect, border_radius=5)
                # Button inner border
                pygame.draw.rect(self.screen, (100, 50, 20), btn_rect, 2, border_radius=5)
                
                color = (255, 255, 255) if hover else (220, 200, 180)
                text = self.font3.render(opt["text"], True, color)
                
                # Center text
                text_center = (SCREEN_SIZE/2 - text.get_width() // 2, y_pos + btn_height/2 - text.get_height() // 2)
                self.screen.blit(text, text_center)

            if selected_idx != last_hovered:
                if self.hover_sound and mouse_moved: # Only play sound on mouse move if we want, or anytime it changes. Let's do anytime it changes to support keyboard sound.
                    self.hover_sound.play()
            last_hovered = selected_idx

            # Handle events
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        selected_idx = (selected_idx - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_idx = (selected_idx + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.click_sound: self.click_sound.play()
                        option = menu_options[selected_idx]["value"]
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        for opt in menu_options:
                            y_pos = SCREEN_SIZE/2 + opt["y_offset"]
                            btn_width, btn_height = 280, 40
                            btn_rect = pygame.Rect(SCREEN_SIZE/2 - btn_width/2, y_pos, btn_width, btn_height)
                            if btn_rect.collidepoint(mouse_pos):
                                if self.click_sound: self.click_sound.play()
                                option = opt["value"]
                                running = False
                if event.type == QUIT:
                    running = False

            pygame.display.flip()

        return option

    def TimeMenu(self):
        menu_options = [
            {"text": "BULLET (1 min)", "y_offset": 10, "value": (60, 0)},
            {"text": "BLITZ (3|2)", "y_offset": 70, "value": (180, 2)},
            {"text": "RAPID (10 min)", "y_offset": 130, "value": (600, 0)},
            {"text": "CLASSICAL (30)", "y_offset": 190, "value": (1800, 0)},
            {"text": "UNLIMITED", "y_offset": 250, "value": None}
        ]

        option = -1
        running = True
        selected_idx = 0
        last_hovered = -1
        last_mouse_pos = pygame.mouse.get_pos()
        
        while running:
            self.update_and_draw_background()

            # Draw central menu panel
            panel_width, panel_height = 420, 400
            panel_rect = pygame.Rect(SCREEN_SIZE/2 - panel_width/2, 45, panel_width, panel_height)
            
            # Outer dark border
            pygame.draw.rect(self.screen, (30, 25, 25), panel_rect, border_radius=5)
            # Inner semi-transparent fill
            s = pygame.Surface((panel_width-10, panel_height-10))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            self.screen.blit(s, (panel_rect.x+5, panel_rect.y+5))
            # Inner gold border
            pygame.draw.rect(self.screen, (200, 150, 80), panel_rect.inflate(-10, -10), 2, border_radius=5)

            # Draw title with glowing effect
            title_text = "TIME CONTROL"
            title_glow = self.font.render(title_text, True, (100, 70, 20))
            title = self.font.render(title_text, True, (255, 230, 150))
            
            title_center = (SCREEN_SIZE/2 - title.get_width() // 2, panel_rect.y + 15)
            self.screen.blit(title_glow, (title_center[0]+2, title_center[1]+2))
            self.screen.blit(title, title_center)

            # Mouse hover effect
            mouse_pos = pygame.mouse.get_pos()
            mouse_moved = (mouse_pos != last_mouse_pos)
            last_mouse_pos = mouse_pos
            
            # Menu options with hover effect
            for idx, opt in enumerate(menu_options):
                y_pos = 130 + idx * 55
                btn_width, btn_height = 280, 40
                btn_rect = pygame.Rect(SCREEN_SIZE/2 - btn_width/2, y_pos, btn_width, btn_height)
                
                if mouse_moved and btn_rect.collidepoint(mouse_pos):
                    selected_idx = idx
                
                hover = (idx == selected_idx)
                
                # Draw glowing aura if hovered
                if hover:
                    aura_rect = btn_rect.inflate(8, 8)
                    pygame.draw.rect(self.screen, (255, 200, 50), aura_rect, border_radius=8)
                
                # Draw wooden button
                pygame.draw.rect(self.screen, (160, 96, 48), btn_rect, border_radius=5)
                # Button inner border
                pygame.draw.rect(self.screen, (100, 50, 20), btn_rect, 2, border_radius=5)
                
                color = (255, 255, 255) if hover else (220, 200, 180)
                text = self.font3.render(opt["text"], True, color)
                
                # Center text
                text_center = (SCREEN_SIZE/2 - text.get_width() // 2, y_pos + btn_height/2 - text.get_height() // 2)
                self.screen.blit(text, text_center)

            if selected_idx != last_hovered:
                if self.hover_sound and mouse_moved:
                    self.hover_sound.play()
            last_hovered = selected_idx

            # Handle events
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return -1
                    elif event.key == pygame.K_UP:
                        selected_idx = (selected_idx - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_idx = (selected_idx + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.click_sound: self.click_sound.play()
                        return menu_options[selected_idx]["value"]
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        for idx, opt in enumerate(menu_options):
                            y_pos = 130 + idx * 55
                            btn_width, btn_height = 280, 40
                            btn_rect = pygame.Rect(SCREEN_SIZE/2 - btn_width/2, y_pos, btn_width, btn_height)
                            if btn_rect.collidepoint(mouse_pos):
                                if self.click_sound: self.click_sound.play()
                                return opt["value"]

            pygame.display.flip()

        return option

    def draw_clocks(self, time_w, time_b, active_player):
        if time_w is None or time_b is None:
            return

        def format_time(ms):
            sec = max(0, ms) / 1000.0
            if sec < 10:
                return f"{sec:.1f}"
            else:
                m = int(sec // 60)
                s = int(sec % 60)
                return f"{m}:{s:02d}"

        text_w = self.font3.render(format_time(time_w), True, (255, 255, 255))
        text_b = self.font3.render(format_time(time_b), True, (255, 255, 255))

        w_rect = pygame.Rect(390, 460, 90, 30)
        b_rect = pygame.Rect(390, 10, 90, 30)

        w_bg = (120, 90, 50) if active_player == 0 else (60, 50, 40)
        b_bg = (120, 90, 50) if active_player == 1 else (60, 50, 40)

        pygame.draw.rect(self.screen, w_bg, w_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 150, 80), w_rect, 2, border_radius=5)
        
        pygame.draw.rect(self.screen, b_bg, b_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 150, 80), b_rect, 2, border_radius=5)

        self.screen.blit(text_w, (w_rect.centerx - text_w.get_width()//2, w_rect.centery - text_w.get_height()//2))
        self.screen.blit(text_b, (b_rect.centerx - text_b.get_width()//2, b_rect.centery - text_b.get_height()//2))

    def Game_player_vs_player(self, board, pieces, time_control=None):
        # player 0 for white
        #        1 for black
        cplayer = ['w', 'b']
        C = [BLUE, BLACK]
        player, cl, st, cmate = 0, -1, [], -1
        last_pos = ()
        running = True
        last_hovered = False
        
        time_w = time_b = None
        inc_ms = 0
        if time_control:
            time_w = time_b = time_control[0] * 1000
            inc_ms = time_control[1] * 1000
        last_tick = pygame.time.get_ticks()

        while running:
            if time_w is not None:
                current_tick = pygame.time.get_ticks()
                delta = current_tick - last_tick
                last_tick = current_tick
                if player == 0:
                    time_w -= delta
                    if time_w <= 0: cmate, running = 101, False
                else:
                    time_b -= delta
                    if time_b <= 0: cmate, running = 100, False
                    
            pos_clicked = ()
            pos = pygame.mouse.get_pos()
            settings_btn = pygame.Rect(10, 10, 80, 30)
            is_hovering = settings_btn.collidepoint(pos)
            if is_hovering and not last_hovered:
                if self.hover_sound: self.hover_sound.play()
            last_hovered = is_hovering
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        settings_btn = pygame.Rect(10, 10, 80, 30)
                        if settings_btn.collidepoint(pos):
                            action = self.handle_settings_menu()
                            if action == 1:
                                return -3
                            elif action == 2:
                                return -2
                            else:
                                continue
                        pos_clicked = rev_rect(pygame.mouse.get_pos())
                        cl += 1
                        if not pieces.precond(pos_clicked, player) and cl == 0:
                            cl -= 1
                            continue
            if pos_clicked != () and not check_valid(pos_clicked[0]-1, pos_clicked[1]-1):
                cl -= 1
                continue
            if pos_clicked != () and cl == 0:
                pieces.selecting(pos_clicked)
                st.append(pos_clicked)
                print_ar(pieces.ar)
            if pos_clicked != () and cl == 1:
                if eq(st[0], pos_clicked):
                    cl -= 1
                    continue
                if pieces.switch_piece(st[0], pos_clicked):
                    cl, st = -1, []
                    clean_selected(pieces.ar)
                    if self.click_sound: self.click_sound.play()
                    continue
                if not pieces.move(pieces.ar, st[0], pos_clicked):
                    cl -= 1
                    continue
                last_pos = (st[0], pos_clicked)
                if self.click_sound: self.click_sound.play()
                
                if time_w is not None:
                    if player == 0: time_w += inc_ms
                    else: time_b += inc_ms
                    
                player, cl, st = 1 - player, -1, []
                print_ar(pieces.ar)
                if pieces.is_checked(pieces.ar, cplayer[player]):
                    if pieces.is_checkmate(pieces.ar, cplayer[player]):
                        cmate = 1-player
                        running = False

            self.update_and_draw_background()
            board.draw_board(C[player])
            pieces.draw_pieces_upgrade(last_pos)
            self.draw_clocks(time_w, time_b, player)

            # Draw Settings button
            if is_hovering:
                pygame.draw.rect(self.screen, (255, 200, 50), settings_btn.inflate(6, 6), border_radius=6)
            
            # Wooden look
            pygame.draw.rect(self.screen, (160, 96, 48), settings_btn, border_radius=5)
            pygame.draw.rect(self.screen, (100, 50, 20), settings_btn, 2, border_radius=5)
            
            font_small = pygame.font.SysFont("Arial", 15, bold=True)
            text_color = (255, 255, 255) if is_hovering else (220, 200, 180)
            settings_text = font_small.render("Settings", True, text_color)
            
            text_rect = settings_text.get_rect(center=settings_btn.center)
            self.screen.blit(settings_text, text_rect)

            pygame.display.flip()
            # self.clock.tick(30)
        return cmate

    # def Game_player_vs_AI(self, board, pieces):
    #     cplayer = ['w', 'b']
    #     C = [BLUE, BLACK]
    #     player, cl, st, cmate = 0, -1, [], -1
    #     last_pos = ()
    #     AI = AI_stupid(pieces.ar, pieces)
    #     running = True
    #     while running:
    #         pos_clicked = ()
    #         for event in pygame.event.get():
    #             if event.type == QUIT:
    #                 running = False
    #             if event.type == MOUSEBUTTONDOWN:
    #                 if player == 0 and pygame.mouse.get_pressed()[0]:
    #                     pos_clicked = rev_rect(pygame.mouse.get_pos())
    #                     cl += 1
    #                     if not pieces.precond(pos_clicked, player) and cl == 0:
    #                         cl -= 1
    #                         continue
    #         if player == 0:
    #             if pos_clicked != () and not check_valid(pos_clicked[0]-1, pos_clicked[1]-1):
    #                 cl -= 1
    #                 continue
    #             if pos_clicked != () and cl == 0:
    #                 pieces.selecting(pos_clicked)
    #                 st.append(pos_clicked)
    #                 print_ar(pieces.ar)
    #             if pos_clicked != () and cl == 1:
    #                 if eq(st[0], pos_clicked):
    #                     cl -= 1
    #                     continue
    #                 if pieces.switch_piece(st[0], pos_clicked):
    #                     cl, st = -1, []
    #                     clean_selected(pieces.ar)
    #                     continue
    #                 if not pieces.move(pieces.ar, st[0], pos_clicked):
    #                     cl -= 1
    #                     continue
    #                 last_pos = (st[0], pos_clicked)
    #                 player, cl, st = 1 - player, -1, []
    #                 print_ar(pieces.ar)
    #                 if pieces.is_checked(cplayer[player]):
    #                     if pieces.is_checkmate(cplayer[player]):
    #                         cmate = 1-player
    #                         running = False
    #         else: # player(AI) = 1
    #             pos = AI.find_pos_random(pieces.ar, pieces, 'b')
    #             pieces.move(pieces.ar, pos[0], pos[1])
    #             print_ar(pieces.ar)
    #             player = 1 - player
    #             last_pos = (pos[0], pos[1])
    #             if pieces.is_checked(cplayer[player]):
    #                 if pieces.is_checkmate(cplayer[player]):
    #                     cmate = 1-player
    #                     running = False
    #         board.draw_board(C[player])
    #         # pieces.draw_pieces()
    #         pieces.draw_pieces_upgrade(last_pos)

    #         pygame.display.flip()
    #         self.clock.tick(30)
    #     return cmate

    def Game_player_vs_AI_Minimax(self, board, pieces, time_control=None):

        cplayer = ['w', 'b']
        C = [BLUE, BLACK]
        player, cl, st, cmate = 0, -1, [], -1
        last_pos = ()
        # AI = AI_Minimax(pieces.ar, pieces)
        AI = AI_Sunfish(pieces.ar, pieces)
        AI_random = AI_stupid(pieces.ar, pieces)
        running = True
        last_hovered = False
        
        time_w = time_b = None
        inc_ms = 0
        if time_control:
            time_w = time_b = time_control[0] * 1000
            inc_ms = time_control[1] * 1000
        last_tick = pygame.time.get_ticks()

        while running:
            if time_w is not None and player == 0:
                current_tick = pygame.time.get_ticks()
                delta = current_tick - last_tick
                last_tick = current_tick
                time_w -= delta
                if time_w <= 0: cmate, running = 101, False

            pos_clicked = ()
            pos = pygame.mouse.get_pos()
            settings_btn = pygame.Rect(10, 10, 80, 30)
            is_hovering = settings_btn.collidepoint(pos)
            if is_hovering and not last_hovered:
                if self.hover_sound: self.hover_sound.play()
            last_hovered = is_hovering
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if player == 0 and pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        settings_btn = pygame.Rect(10, 10, 80, 30)
                        if settings_btn.collidepoint(pos):
                            action = self.handle_settings_menu()
                            if action == 1:
                                return -3
                            elif action == 2:
                                return -2
                            else:
                                continue
                        pos_clicked = rev_rect(pygame.mouse.get_pos())
                        # print(pos_clicked)
                        cl += 1
                        if not pieces.precond(pos_clicked, player) and cl == 0:
                            cl -= 1
                            continue
            if player == 0:
                if pos_clicked != () and not check_valid(pos_clicked[0]-1, pos_clicked[1]-1):
                    cl -= 1
                    continue
                if pos_clicked != () and cl == 0:
                    pieces.selecting(pos_clicked)
                    st.append(pos_clicked)
                    # print_ar(pieces.ar)
                if pos_clicked != () and cl == 1:
                    if eq(st[0], pos_clicked):
                        cl -= 1
                        continue
                    if pieces.switch_piece(st[0], pos_clicked):
                        cl, st = -1, []
                        clean_selected(pieces.ar)
                        if self.click_sound: self.click_sound.play()
                        continue
                    if not pieces.move(pieces.ar, st[0], pos_clicked):
                        cl -= 1
                        continue
                    last_pos = (st[0], pos_clicked)
                    if self.click_sound: self.click_sound.play()
                    
                    if time_w is not None: time_w += inc_ms
                    
                    player, cl, st = 1 - player, -1, []
                    # print("Is WK moved? ", pieces.prev_move.is_king_moved('w'))
                    # print_ar(pieces.ar)
                    if pieces.is_checked(pieces.ar, cplayer[player]):
                        if pieces.is_checkmate(pieces.ar, cplayer[player]):
                            cmate = 1-player
                            running = False
            else: # player(AI) = 1 ar,pieces,type,alpha,beta,depth, last_move):
                start_ai_tick = pygame.time.get_ticks()
                pos = AI.minimax(pieces.ar,pieces,'b',-1000000000,1000000000,3,None,pieces.prev_move)
                
                if time_b is not None:
                    ai_time = pygame.time.get_ticks() - start_ai_tick
                    time_b -= ai_time
                    if time_b <= 0:
                        cmate = 100
                        running = False
                    else:
                        time_b += inc_ms
                    last_tick = pygame.time.get_ticks()

                if pos[1] == None:
                    p_random = AI_random.find_pos_random(pieces.ar, pieces, 'b')
                    if p_random == None:
                        cmate = 2
                        running = False
                    else:
                        print("It's confused\n")
                        pieces.move(pieces.ar, p_random[0], p_random[1])
                        if self.click_sound: self.click_sound.play()
                else:
                    pieces.selecting(pos[1])
                    pieces.move(pieces.ar, pos[1], pos[2])
                    print_ar(pieces.ar)
                    print(AI.eval_board(pieces.ar), pos[0],"\n")
                    last_pos = (pos[1], pos[2])
                    if self.click_sound: self.click_sound.play()
                    player = 1 - player
                    if pieces.is_checked(pieces.ar, cplayer[player]):
                        if pieces.is_checkmate(pieces.ar, cplayer[player]):
                            cmate = 1-player
                            running = False
            self.update_and_draw_background()
            board.draw_board(C[player])
            # pieces.draw_pieces()
            pieces.draw_pieces_upgrade(last_pos)
            self.draw_clocks(time_w, time_b, player)

            # Draw Settings button
            if is_hovering:
                pygame.draw.rect(self.screen, (255, 200, 50), settings_btn.inflate(6, 6), border_radius=6)
            
            # Wooden look
            pygame.draw.rect(self.screen, (160, 96, 48), settings_btn, border_radius=5)
            pygame.draw.rect(self.screen, (100, 50, 20), settings_btn, 2, border_radius=5)
            
            font_small = pygame.font.SysFont("Arial", 15, bold=True)
            text_color = (255, 255, 255) if is_hovering else (220, 200, 180)
            settings_text = font_small.render("Settings", True, text_color)
            
            text_rect = settings_text.get_rect(center=settings_btn.center)
            self.screen.blit(settings_text, text_rect)

            pygame.display.flip()
            # self.clock.tick(20)
        return cmate

    def Game_Over(self, board, pieces, cmate):
        if cmate == -1:
            txt = "-= Never Give Up =-"
        elif cmate == 2:
            txt = "-= Draw =-"
        elif cmate == 100:
            txt = "-= WHITE WON ON TIME =-"
        elif cmate == 101:
            txt = "-= BLACK WON ON TIME =-"
        else:
            txt = "-= PLAYER "+str(cmate+1)+" WON! =-"
        txt = self.font.render(txt, True, GREEN)
        txt_center = (
            SCREEN_SIZE/2 - txt.get_width() // 2,
            50//2 - txt.get_height() // 2
        )
        font_small = pygame.font.SysFont("Arial", 20)
        txt2 = font_small.render("Click anywhere to continue", True, WHITE)
        txt2_center = (SCREEN_SIZE/2 - txt2.get_width() // 2, SCREEN_SIZE/2 + 200)

        running = True
        return_val = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    return_val = False
                if event.type == MOUSEBUTTONDOWN:
                    running = False

            self.update_and_draw_background()
            board.draw_board(BLUE)
            pieces.draw_pieces()
            self.screen.blit(txt, txt_center)
            self.screen.blit(txt2, txt2_center)

            pygame.display.flip()
        
        return return_val
            # self.clock.tick(30)



if __name__ == '__main__':
    t = Game()
    t.run()

