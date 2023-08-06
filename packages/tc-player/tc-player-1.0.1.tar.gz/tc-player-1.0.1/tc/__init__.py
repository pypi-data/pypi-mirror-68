from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


INTERVAL = 0.05


class TCException(RuntimeError):
    tc_message = None

    def __init__(self, message=None, *a, **k):
        super().__init__(message or self.tc_message, *a, **k)


class TCLoginException(TCException):
    tc_message = 'Failed to log in; please check your Time Gamers credentials.'


class TCLoadException(TCException):
    tc_message = (
        "Couldn't load the Time Gamers website. "
        "Maybe your network connection is down?"
    )


def get_driver(visible):
    options = webdriver.ChromeOptions()
    if not visible:
        options.add_argument('headless')
    options.add_argument('window-size=1200x800')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def click_at_ratio(action, frame, x, y):
    height = frame.size['height']
    width = frame.size['width']
    action.move_to_element_with_offset(frame, width * x, height * y)
    action.click()
    action.pause(INTERVAL)


def loop(driver):
    frame = driver.find_element_by_id('unityFrame')

    while True:
        action = ActionChains(driver)

        click_at_ratio(action, frame, .5, .5)

        for i in range(200):
            action.click()
            action.pause(INTERVAL)

        # click all the upgrade buttons
        click_at_ratio(action, frame, 0.05, .3)
        click_at_ratio(action, frame, 0.05, .45)
        click_at_ratio(action, frame, 0.05, .6)
        click_at_ratio(action, frame, 0.05, .7)
        click_at_ratio(action, frame, 0.05, .85)

        # click 'activate all'
        click_at_ratio(action, frame, 0.95, .7)

        # click dimension shift
        click_at_ratio(action, frame, 0.83, .62)

        # click cooldown
        click_at_ratio(action, frame, 0.97, .62)

        action.perform()


def _tc(driver, username, password):
    driver.get('http://www.timegamers.com/login/')

    try:
        form = driver.find_element_by_id('pageLogin')
    except NoSuchElementException:
        raise TCLoadException()

    form.find_element_by_id('ctrl_pageLogin_login').send_keys(username)
    form.find_element_by_id('ctrl_pageLogin_password').send_keys(password)
    form.find_element_by_css_selector('[type=submit]').click()
    try:
        driver.find_element_by_css_selector('.navTab.account')
    except NoSuchElementException:
        raise TCLoginException()

    driver.get('http://www.timegamers.com/TimeClickers/WebGL/#unityFrame')

    print('waiting thirty seconds for the game to load')
    sleep(30)

    frame = driver.find_element_by_id('unityFrame')
    action = ActionChains(driver)

    # click play
    click_at_ratio(action, frame, .5, .55)
    action.pause(20)  # another unchecked load wait

    click_at_ratio(action, frame, .25, .05)  # open settings
    click_at_ratio(action, frame, .04, .23)  # disable screen shake
    click_at_ratio(action, frame, .04, .38)  # reduce particles
    click_at_ratio(action, frame, .04, .45)  # disable post effects
    click_at_ratio(action, frame, .04, .6)  # reduce framerate
    click_at_ratio(action, frame, .25, .05)  # close settings

    # turn idle mode on for weapons
    click_at_ratio(action, frame, .29, .96)  # launcher
    click_at_ratio(action, frame, .45, .96)  # cannon
    click_at_ratio(action, frame, .71, .96)  # pistol

    # set upgrade mode to max
    for i in range(3):
        click_at_ratio(action, frame, .03, .95)

    print('setting things up')
    action.perform()

    print('running loop!')
    loop(driver)


def tc(username, password, visible=False):
    driver = get_driver(visible)
    try:
        _tc(driver, username, password)
    finally:
        driver.quit()
