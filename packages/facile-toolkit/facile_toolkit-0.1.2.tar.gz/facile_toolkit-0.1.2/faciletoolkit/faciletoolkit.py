"""

Robot library with often needed keywords.

BuiltIn Robot Framework's standard library that provides a set of generic 
keywords needed often to deal with facile.it projects.

This library could be easily extended to other projects as It's an open source 
project.

The provided keywords can be used, for example, instanciating browsers:

e.g. facile.toolkit.open_mobile_browser  facile.it  Galaxy S5

Then the test will run against the given bundle above, start url desired 
and its device.

Also a couple of js execution capabilities like scroll, 
javascript_click_webelement and etc...


"""

import random
import datetime
import os
import selenium
from selenium import webdriver
from robot.api import logger
from robot.api.deco import keyword
from robot.errors import RobotError
from robot.libraries.BuiltIn import BuiltIn

from robot.utils import (DotDict, escape, format_assign_message,
                         get_error_message, get_time, html_escape, is_falsy, is_integer,
                         is_string, is_truthy, is_unicode, IRONPYTHON, JYTHON,
                         Matcher, normalize, NormalizedDict, parse_time, prepr,
                         plural_or_not as s, PY3, RERAISED_EXCEPTIONS, roundup,
                         secs_to_timestr, seq2str, split_from_equals, StringIO,
                         timestr_to_secs, type_name, unic, is_list_like)
from robot.errors import (ContinueForLoop, DataError, ExecutionFailed,
                          ExecutionFailures, ExecutionPassed, ExitForLoop,
                          PassExecution, ReturnFromKeyword)


class Error(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True


class faciletoolkit:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
    
    @staticmethod
    @keyword
    def wait(keyword, *keywordargs): 
        """Automatically retries the given keywords/arguments 10 times, each 3 seconds
        """
        BuiltIn().wait_until_keyword_succeeds("10 x", "3 s", keyword, *keywordargs)
 
    
    @staticmethod
    @keyword
    def field_returns(validity):
        """ Returns DOM error status based on Facile "err wrong" class.
        
            "Validity" set to "invalid" expects the error to pop hence passes the test.
            "Validity" set to "Valid" expects the error to not pop
        """

        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        source = driver.page_source
        validity = validity.lower()
        if validity == "invalid" and "err wrong" in source:
            logger.info(source)
        elif validity == "invalid" and "err wrong" not in source:
            raise(RobotError("err wrong is in source"))
        elif validity == "valid" and "err wrong" not in source:
            logger.info(source)
        elif validity == "valid" and "err wrong" in source:
            raise(RobotError("source contains 'err wrong' sub-string"))
            
    @staticmethod
    @keyword
    def open_browser(url, browser):
        """ Opens the given browser and goes on url.
            browser may be Firefox or Chrome. Firefox may be passed as "ff" aswell.
        """
        browser = browser.lower()
        session = BuiltIn().get_library_instance('SeleniumLibrary')
        if browser == "chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-browser-side-navigation")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.set_capability("pageLoadStrategy", "eager")
            session.open_browser(url, browser, options=chrome_options)
        elif browser == "firefox" or "ff":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-gpu")
            firefox_options.add_argument("--disable-extensions")
            firefox_options.add_argument("--ignore-certificate-errors")
            firefox_options.set_capability("pageLoadStrategy", "eager")
            session.open_browser(url, browser, options=firefox_options)
        else:
            raise RobotError("unexpected")
    
    @staticmethod
    @keyword
    def open_mobile_browser(url, device):
        """ Opens a mobile-emulated chrome session based on the given device and 
            goes to the given url.
        """
        session = BuiltIn().get_library_instance('SeleniumLibrary')
        chrome_options = webdriver.ChromeOptions()
        mobile_emulation = {"deviceName": device}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-browser-side-navigation")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.set_capability("pageLoadStrategy", "eager")
        session.open_browser(url, "Chrome", options=chrome_options)

    @staticmethod
    @keyword
    def element_attribute_should_contain_value(element, attribute, value):
        """ 
        Returns PASS status if the given element's attribute contains the inputed value.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        attr = driver.get_element_attribute(element, attribute)
        try:
            BuiltIn().should_contain(attr, value)
        except Exception as error_thrown:
            raise RobotError(error_thrown)

    @staticmethod
    @keyword
    def element_attribute_should_not_contain_value(element, attribute, value):
        """ 
            Returns PASS status if the given element's attribute does not contain the inputed value.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        attr = driver.get_element_attribute(element, attribute )
        try:
            BuiltIn().should_not_contain(attr, value)
        except Exception as error_thrown:
            raise RobotError(error_thrown)
        
    @staticmethod
    @keyword
    def clear_session():
        """
        This keyword cleans the current session in order to isolate the execution
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.delete_all_cookies()
        driver.reload_page()

    @staticmethod
    @keyword
    def scroll(range="0"):
        """ Scrolls the document.

            Ranges might span between 0 to X where 0 is the beginning of the document.

            default is set to 0.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.execute_javascript("document.documentElement.scrollTop = "+range+";")

    @staticmethod
    @keyword
    def dom_is_loaded(timeout="5s"):
        """ 
        returns True if DOM readyState equals "complete" before the given timeout.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.wait_for_condition("return document.readyState=='complete'", timeout)

    @staticmethod
    @keyword
    def checkpoint(locator, timeout="60s"):
        """Waits for a maximum time, defined by timeout argument (default=60s),
           until a webelement (defined by a locator) is contained on the page and displayed
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        faciletoolkit().dom_is_loaded(timeout)
        driver.wait_until_page_contains_element(locator, timeout)
        driver.wait_until_element_is_visible(locator, timeout)
        #da vedere se EC wrappa due condition in una e wrappare i due wait
        log_preventivo = BuiltIn().run_keyword_and_return_status("should_contain", locator, "AS_result_content", None, True, False)
        if log_preventivo:
            faciletoolkit().I_log_id_preventivo()
    
    @staticmethod
    @keyword
    def I_log_id_preventivo():
        """
        checks if the given Id Preventivo is present on the page
        and logs it to a csv file located in the default output folder
        """
        Suite = BuiltIn().get_variable_value("${SUITE_NAME}")
        Test = BuiltIn().get_variable_value("${TEST_NAME}")
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        status, id_preventivo = BuiltIn().run_keyword_and_ignore_error("Execute_javascript", "return AS_Preventivo.ID_PREV")
        logger.console("\nid preventivo: %s" % id_preventivo)
        date = datetime.datetime.now()
        pwd = os.getcwd()
        nome_file = pwd + "/id_preventivi.csv"
        check = os.path.exists(nome_file)
        try:
            if "JavascriptException" not in id_preventivo and check:
                f = open(nome_file, "w+", encoding="UTF-8")
                f.write("{}, {}, {}, {}\n".format(date, Suite, Test, id_preventivo))
                f.close()
            elif "JavascriptException" not in id_preventivo and check == False:
                logger.console("%s not accessible, creating new log file " % nome_file)
                file_preventivo = open(nome_file, "w+", encoding="UTF-8")
                file_preventivo.write("{}, {}, {}, {}\n"
                                    .format(date, Suite, Test, id_preventivo))
                file_preventivo.close()
        except Exception and IOError as e:
            raise Error(status)
                

    @staticmethod
    @keyword
    def select_from_list_random_index(locator, start_index=1):
        """
        Selects a random option from a Select WebElement specified by a locator,
        it is possible to specify a start index for the random selection
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        faciletoolkit().dom_is_loaded()
        element = driver.get_webelement(locator)
        element_id = driver.get_element_attribute(element, "id")
        BuiltIn().run_keyword_and_ignore_error("Checkpoint", "//*[@id='"+element_id+"']//option[string-length(@value)>0]", "10s")
        list_length = driver.execute_javascript("return arguments[0].options.length", "ARGUMENTS",  element)
        logger.info(str(list_length) + " " +  element_id)
        if list_length == 1:
            return "null"
        random_index = random.randint(start_index, list_length-1)
        random_index = str(random_index)
        driver.select_from_list_by_index(locator, random_index)
    
    @staticmethod
    @keyword
    def select_from_list_random_index_optional(*locators):
        """
        Wrapper for "select from list random index" keyword, the random selection
        is performed only if the select element is present on the page
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        for locator in locators:
            lista_presente = BuiltIn().run_keyword_and_return_status("checkpoint", locator, "2s")
            if lista_presente:
                faciletoolkit().select_from_list_random_index(locator)

    @staticmethod
    @keyword
    def I_land_on_page(url, timeout="60s"):
        """
        Waits for a maximum time, defined by timeout argument (default=60s),
        until the location contains a portion of the url (specified by the parameter 'url')
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.wait_for_condition("return document.location.href.includes('%s')" % url, timeout)
        faciletoolkit().dom_is_loaded()

    @staticmethod
    @keyword
    def javascript_click_TA(locator):
        """
        This keyword clicks a WebElement or a locator that represent a WebElement via Javascript
        """
        is_webelement = isinstance(locator, selenium.webdriver.remote.webelement.WebElement)
        if is_webelement:
            faciletoolkit().Javascript_Click_WebElement(locator)
        else:
            faciletoolkit().Javascript_Click_by_Locator(locator)
    
    @staticmethod
    @keyword
    def Javascript_Click_WebElement(element):
        """
        This keyword clicks a WebElement via Javascript
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.execute_javascript("arguments[0].click()", "ARGUMENTS", element)

    @staticmethod
    @keyword
    def Javascript_Click_by_Locator(locator):
        """
        Clicks a locator that represent a WebElement via Javascript
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        element = driver.get_webelement(locator)
        driver.execute_javascript("arguments[0].click()", "ARGUMENTS", element)    

    @staticmethod
    @keyword
    def check_page_locators(*locators):
        """
        Loops over an array of locators and checks
        if the webelements represented by them are visible on the page
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        errors = []
        for i in locators:
            try:
                driver.element_should_be_visible(i)
            except Exception as e:
                errors.append(str(e))
        if len(errors) > 0:
            BuiltIn().fail("\n".join(errors))
    
    @staticmethod
    @keyword
    def Select_first_autocomplete_option():
        """
        Selects the first autocomplete option for auto-complete fields.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        locator_option = "css:.autocomplete-suggestions:not([style*='display']):not([style*='none']) strong"
        BuiltIn().run_keyword_and_ignore_error("Checkpoint", locator_option, "2s")
        try:
            return 'PASS', BuiltIn().run_keyword("faciletoolkit.wait", "Javascript_click_ta", locator_option)
        except ExecutionFailed as err:
            if err.dont_continue:
                raise
            return 'FAIL', unic(err)

    @staticmethod
    @keyword
    def get_right_locator(*locators, checkpoint_timeout="200ms"):
        """
        Returns the first locator that exist and is visible
        on the page from a list of locators/WebElements
        """
        for locator in locators:
            try:
                exists = BuiltIn().run_keyword_and_return_status(
                    "Checkpoint", locator, checkpoint_timeout)
                if exists:
                    return locator
            except Exception as error_thrown:
                raise Error(error_thrown)

            

    @staticmethod
    @keyword
    def press_key_on_active_element(key):
        """
        Inputs the given key to the active element in DOM
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        active_element = driver.execute_javascript("return document.activeElement;")
        driver.press_keys(active_element, key)
    
    @staticmethod
    @keyword
    def wait_for_autocomplete_visibility_to_be(loaded):
        """
        Lets the driver wait until the autocomplete div 
        is visible (True) / hidden (False)
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        locator_autocomplete = "//div[@class='autocomplete-suggestions' and not(contains(@style,'display: none'))]"
        if loaded:
            driver.wait_until_page_contains_element(locator_autocomplete)
        else:
            driver.wait_until_page_does_not_contain_element(locator_autocomplete)
    
    @staticmethod
    @keyword
    def get_text_from_webelements(*webelements):
        """
        Takes in input a WebElements array and
        returns a string array containing the stripped texts retrieved from the webelements
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        text_list = []
        for element in webelements:
            text = driver.get_text(element)
            text = text.strip()
            text_list.append(text)
        return text_list

    @staticmethod
    @keyword
    def generate_random_number_as_string(minimum, maximum):
        """
        Generates a random number between the range given by "min", "max" arguments
        and returns it as string
        """
        num = str(random.randint(minimum, maximum))
        return num

    @staticmethod
    @keyword
    def select_random_item_from_list(*lists):
        """
        Returns a random item from the given list
        """
        item = random.choice(lists)
        return item

    @staticmethod
    @keyword
    def I_click_the_button_prosegui():
        """
        This keyword check if "Prosegui" button is present and visible, then clicks it
        """
        button = "id:pulsanteAvanti"
        faciletoolkit().checkpoint(button)
        faciletoolkit().javascript_click_TA(button)

    @staticmethod
    @keyword
    def check_if_error_message_is_present_on_page(message):
        """
        Checks if the given error message is present in DOM
        """
        try:
            faciletoolkit().checkpoint("//span[contains(.,'%s') and contains(@class,'err wrong')]" % message, "5s" )
            logger.info("%s is contained in error message" % message)
        except Exception as error_thrown:
            raise Error(error_thrown)