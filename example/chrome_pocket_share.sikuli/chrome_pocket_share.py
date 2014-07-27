import unittest
from andwalker import MonkeySikuliDevice

CHROME_PACKAGE = 'com.android.chrome'
POCKET_PACKAGE = 'com.ideashower.readitlater.pro'

class ChromePocketTest(unittest.TestCase):

    def setUp(self):
        self._device = MonkeySikuliDevice(DEVICE_SERIAL_NUMBER, SCREEN)
        self.reset_pocket()
        self._device.open_app(CHROME_PACKAGE)

    def test_chrome_pocket_share(self): 
        if not exists("chrome_tabs_button_none.png"): self.close_all_tabs()
        tap("chrome_new_tab_button.png")
        type("chrome_address_bar.png", 'gtac2014')
        tap("keyboard_go.png") # soft keyboard
        tap(Pattern("chrome_search_result.png").targetOffset(-123,-17))
        wait("gtac_banner.png")
        pressMenu()
        tap("chrome_share_menu.png")
        tap("chrome_add_to_pocket.png")
        tap("pocket_icon_float.png") # then Pocket opens
        assert exists("pocket_list.png")

    def reset_pocket(self):
        """To make sure Pocket is initialized and the list is empty."""
        self._device.clear_app(POCKET_PACKAGE)
        self._device.open_app(POCKET_PACKAGE,
            'com.ideashower.readitlater.activity.AppCacheCheckActivity')
        tap("pocket_login.png")
        type("pocket_username.png",'<YOUR_ACCOUNT_HERE>')
        type("pocket_password.png", '<YOUR_PASSWORD_HERE>')
        tap("pocket_login_yellow.png")
        wait("pocket_welcome.png")
        for _ in range(3):
            tap("pocket_next.png")
        tap("pocket_view_your_list.png")
        wait("pocket_list_is_empty.png")

    def close_all_tabs(self):
        """For the sake of demostartion, because the UI for switching tabs
           is not accessible.
        """
        tap(Pattern("chrome_tabs_button.png").targetOffset(53,5)) # target offset
        for _ in findAll("chrome_tab_close.png"):
            tap("chrome_tab_close.png")
        assert exists("chrome_tabs_button_none.png")

if __name__ == '__main__':
    unittest.main()

