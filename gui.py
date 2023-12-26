"""CSC110 Fall 2021: Course Project

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Brian Wang, Yahya Elgabra, Kareem Salem, Wenqi Zhan.
"""

# Import necessary modules
import pygame
import sys
from process_data import load_articles, display_graph
from overall_report_stats import get_overall_statistics

# Declare color variables
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (212, 175, 55)
COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)


class Visual:
    """
    An abstract class representing a visual representation in the GUI.

    Instance Attributes:
        - screen: the screen visuals are displayed in
        - font: the font of the visual
        - message: the font of the visual
        - color: the rgb color code of the visual
        - width: the width of the visual
        - height: the height of the visual
        - x: x coordinate of the visual, initialized to 0
        - y: y coordinate of the visual, initialized to 0
    """
    screen: pygame.Surface
    font: pygame.font.Font
    section_id: str
    message: str
    color: tuple[int, int, int]
    text: pygame.font
    width: float
    height: float
    x: float
    y: float

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, message: str, color: tuple[int, int, int]) -> None:
        self.screen = screen
        self.font = font
        self.message = message
        self.color = color
        self.text = font.render(message, True, color)
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        self.x = 0
        self.y = 0


class Text(Visual):
    """ A subclass of Visual representing the text displayed in the GUI
    """

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, message: str, color: tuple) -> None:
        Visual.__init__(self, screen, font, message, color)

    def display_text(self, x: float, y: float) -> None:
        """ Set the x and y coordinate for the text and display it onto the screen
        """
        self.x = x
        self.y = y
        self.screen.blit(self.text, (x, y))


class Button(Visual):
    """ A subclass of Visual representing the buttons displayed in the GUI

    Instance Attributes:
        - rect: the pygame rect object of the button
        - button_color: rgb color of button background, initialized to RED
        - border_color: rgb color of button border, initialized to BLACK
        - border_thickness: the thickness of the button border, initialized to 3
        - hover: weather or not the button is being hovered over, initialized to False
    """
    rect: pygame.rect.Rect
    button_color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    border_thickness: int
    hover: bool

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, message: str, color: tuple) -> None:
        Visual.__init__(self, screen, font, message, color)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_color = RED
        self.border_color = BLACK
        self.border_thickness = 3
        self.hover = False

    def display_button(self, x: float, y: float) -> None:
        """Set the x and y coordinate for the button and display it onto the screen
        """
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.button_color, self.rect, 0)
        pygame.draw.rect(self.screen, self.button_color, self.rect, self.border_thickness)
        self.screen.blit(self.text, (self.x, self.y))

    def mouse_hover(self, mouse_x: float, mouse_y: float) -> tuple[bool, tuple]:
        """Detect if the mouse position hovers over a button or not and return if it is and green to change the color
        """
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True, GREEN
        else:
            return False, RED


# Code here retrieved from stack overflow, see references
class DropDown:
    """Drop down class representing the dropdowns displayed in the GUI

    Instance Attributes:
        - color_menu: a list of all the drop down menu rgb colors
        - color_option: a list of all the drop down option rgb colors
        - width: the width of the dropdown
        - height: the height of the dropdown
        - x: x coordinate of the dropdown, initialized to 0
        - y: y coordinate of the dropdown, initialized to 0
        - rect: the pygame rect object of the dropdown
        - font: the font of the dropdown
        - main: beginning dropdown selected value
        - options: dropdown options to select from
        draw_menu: weather the program can draw the menu or not is available or not, initialized to False
        menu_active: weather an menu is available or not, initialized to False
        active_option: weather an option is available or not, initialized to -1
    """
    color_menu: list[tuple[int, int, int]]
    color_option: list[tuple[int, int, int]]
    width: int
    height: int
    font: pygame.font.Font
    main: str
    options: list[str]
    color: tuple[int, int, int]
    text: pygame.font
    x: float
    y: float
    rect: pygame.rect.Rect
    draw_menu: bool
    active_option: int

    def __init__(self, color_menu: list[tuple[int, int, int]], color_option: list[tuple[int, int, int]], width: int,
                 height: int, font: pygame.font.Font, main: str, options: list[str]) -> None:
        self.color_menu = color_menu
        self.color_option = color_option
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def display_dropdown(self, surf: pygame.Surface, x: float, y: float) -> None:
        """
        Set the x and y coordinate for the dropdown and display it onto the screen
        """
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, True, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, dropdown_text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(dropdown_text, True, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list: list) -> int:
        """Get the position of the mouse and update the dropdown based on the choice
        """
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1


def main_loop() -> None:
    # Initialize pygame
    pygame.init()

    # Declare screen size and caption
    screen_size = (1000, 600)
    screen = pygame.display.set_mode(screen_size, 0)
    pygame.display.set_caption("CSC110 Final Project")

    # Declare screen width and height
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Define Font variables
    title = pygame.font.SysFont("arial", 40)
    text = pygame.font.SysFont("arial", 25)
    margin = 50

    # Load articles
    articles = load_articles()

    # Create GUI Button, Text, and Dropdown objects
    menu_button = Button(screen, title, "Menu", BLACK)
    overall_report_button = Button(screen, title, "Overall Report", BLACK)
    media_progression_button = Button(screen, title, "Interactive Graph", BLACK)
    back_button = Button(screen, text, "BACK", BLACK)
    graph_button = Button(screen, title, "GRAPH", BLACK)

    title_screen = Text(screen, title, "Analysis of Public Health Discussion in The News over Time", GOLD)
    title_caption = Text(screen, text, "Brian Wang, Yahya Elgabra, Kareem Salem, Wenqi Zhan", BLACK)
    title_menu = Text(screen, title, "Main Menu", GOLD)
    welcome_text = \
        Text(screen, text,
             "Welcome to the COVID-19 news indicator, select an option for the type of data analysis.", BLACK)
    overall_report_text = Text(screen, text,
                               "Select Overall Report to get general statistics of the pandemic in the news", BLACK)
    interactive_graph_text = \
        Text(screen, text,
             "Select Interactive Graph for a graph of COVID-19 news prevalence with time and genre specifics", BLACK)
    interactive_graph_screen_title = Text(screen, title, "Interactive Graph", GOLD)
    overall_report_screen_title = Text(screen, title, "Overall Report", GOLD)

    stats = get_overall_statistics(articles)
    avgs = {key: stats[key][1] for key in stats}

    average_influence = stats['all'][1]
    most_affected_genre = max(avgs, key=avgs.get)
    least_affected_genre = min(avgs, key=avgs.get)
    percentage = round(stats['all'][2] / stats['all'][0], 2)
    average_influence_text = Text(screen, text,
                                  f"The average influence score (0 - 6): {round(average_influence, 2)}", BLACK)
    most_affected_text = Text(screen, text, f"{most_affected_genre} was the most affected genre with a score of: "
                                            f"{round(stats[most_affected_genre][1], 2)}", BLACK)
    least_affected_text = Text(screen, text, f"{least_affected_genre} was the least affected genre with a score of: "
                                             f"{round(stats[least_affected_genre][1], 2)}", BLACK)
    percentage_text = Text(screen, text, f"The percentage of Covid-19 articles (average influence score > 3.5): "
                                         f"{percentage*100}%", BLACK)

    genres = ["All Genres", 'Science and Technology', 'Business', 'Politics and Global News',
              'Miscellaneous News', 'Culture', 'Other']
    genre_list = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], 300, 50,
        text,
        "All Genres", genres)
    times = ["All Time", "6 Months", "1 Month", "1 Weeks"]
    time_list = DropDown(
        [COLOR_INACTIVE, COLOR_ACTIVE],
        [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE], 300, 50,
        text,
        "All Time", times)

    current_buttons_selected = [0, 0]

    # Initialize screen values
    start_screen = True
    menu_screen = False
    overall_report_screen = False
    interactive_graph_sreen = False
    screen.fill(WHITE)
    pygame.display.update()

    # Main program loop
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False

            mouse_x, mouse_y = pygame.mouse.get_pos()
            menu_button.hover, menu_button.button_color = menu_button.mouse_hover(mouse_x, mouse_y)
            if event.type == pygame.MOUSEBUTTONDOWN and menu_button.hover:
                menu_screen = True
                menu_button.hover = False

        title_screen.display_text(screen_width / 2 - title_screen.width / 2,
                                  screen_height / 2 - 2 * title_screen.height)
        title_caption.display_text(screen_width / 2 - title_caption.width / 2,
                                   title_screen.y + title_caption.height + margin)
        menu_button.display_button(screen_width / 2 - menu_button.width / 2,
                                   screen_height - menu_button.height * 2 - margin)
        pygame.display.update()

        while menu_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_screen = False
                    menu_screen = False

                mouse_x, mouse_y = pygame.mouse.get_pos()
                overall_report_button.hover, overall_report_button.button_color = \
                    overall_report_button.mouse_hover(mouse_x, mouse_y)
                media_progression_button.hover, media_progression_button.button_color = \
                    media_progression_button.mouse_hover(mouse_x, mouse_y)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if overall_report_button.hover:
                        overall_report_screen = True
                        overall_report_button.hover = False
                    elif media_progression_button.hover:
                        interactive_graph_sreen = True
                        media_progression_button.hover = False

            screen.fill(WHITE)
            title_menu.display_text(screen_width / 2 - title_menu.width / 2, title_screen.height)
            welcome_text.display_text(margin, title_menu.y + welcome_text.height + margin)
            overall_report_text.display_text(margin, welcome_text.y + overall_report_text.height + margin)
            interactive_graph_text.display_text(margin, overall_report_text.y + interactive_graph_text.height + margin)
            overall_report_button.display_button(margin,
                                                 interactive_graph_text.y + overall_report_button.height + margin)
            media_progression_button.display_button(screen_width / 2,
                                                    interactive_graph_text.y + overall_report_button.height + margin)
            pygame.display.update()

            while overall_report_screen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        start_screen = False
                        menu_screen = False
                        overall_report_screen = False

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    back_button.hover, back_button.button_color = back_button.mouse_hover(mouse_x, mouse_y)
                    if event.type == pygame.MOUSEBUTTONDOWN and back_button.hover:
                        overall_report_screen = False
                        back_button.hover = False

                screen.fill(WHITE)
                back_button.display_button(0, 0)
                overall_report_screen_title.display_text(screen_width / 2 - overall_report_screen_title.width / 2,
                                                         margin / 2)
                average_influence_text.display_text(
                    margin, overall_report_screen_title.y + overall_report_screen_title.height + margin)
                most_affected_text.display_text(
                    margin, average_influence_text.y + average_influence_text.height + margin)
                least_affected_text.display_text(margin, most_affected_text.y + most_affected_text.height + margin)
                percentage_text.display_text(margin, least_affected_text.y + least_affected_text.height + margin)
                pygame.display.update()

            while interactive_graph_sreen:
                event_list = pygame.event.get()
                for event in event_list:
                    if event.type == pygame.QUIT:
                        start_screen = False
                        menu_screen = False
                        interactive_graph_sreen = False

                    selected_genre = genre_list.update(event_list)
                    if selected_genre >= 0:
                        genre_list.main = genre_list.options[selected_genre]
                        current_buttons_selected[0] = selected_genre

                    selected_time = time_list.update(event_list)
                    if selected_time >= 0:
                        time_list.main = time_list.options[selected_time]
                        current_buttons_selected[1] = selected_time

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    back_button.hover, back_button.button_color = back_button.mouse_hover(mouse_x, mouse_y)
                    graph_button.hover, graph_button.button_color = graph_button.mouse_hover(mouse_x, mouse_y)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if back_button.hover:
                            interactive_graph_sreen = False
                            back_button.hover = False
                        elif graph_button.hover:
                            display_graph((current_buttons_selected[0], current_buttons_selected[1]), articles)

                screen.fill(WHITE)
                back_button.display_button(0, 0)
                interactive_graph_screen_title.display_text(
                    screen_width / 2 - interactive_graph_screen_title.width / 2, margin / 2)
                genre_list.display_dropdown(
                    screen, margin, interactive_graph_screen_title.y + interactive_graph_screen_title.height + margin)
                time_list.display_dropdown(
                    screen, genre_list.x + genre_list.width + margin,
                    interactive_graph_screen_title.y + interactive_graph_screen_title.height + margin)
                graph_button.display_button(time_list.x + time_list.width + margin,
                                            interactive_graph_screen_title.y +
                                            interactive_graph_screen_title.height + margin)
                pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'sys', 'process_data', 'overall_report_stats'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
