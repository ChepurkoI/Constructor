# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import re
from collections.abc import Iterable
from typing import Any
from typing import Callable
from typing import List
from typing import Literal
from typing import Tuple
from typing import TypeVar
from typing import Union

from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement

"""
 * Готовые "Ожидаемые условия", которые обычно полезны в webdriver
 * tests.
"""

D = TypeVar("D")
T = TypeVar("T")

WebDriverOrWebElement = Union[WebDriver, WebElement]


def title_is(title: str) -> Callable[[WebDriver], bool]:
    """Ожидание для проверки заголовка страницы.

    title - ожидаемый заголовок, который должен точно совпадать.
    True, если заголовок совпадает, false в противном случае.
    """

    def _predicate(driver: WebDriver):
        return driver.title == title

    return _predicate


def title_contains(title: str) -> Callable[[WebDriver], bool]:
    """Ожидание для проверки того, что заголовок содержит подстроку, чувствительную к регистру. 
    title - фрагмент заголовка, ожидаемое возвращает True, если заголовок совпадает, False в противном случае"""

    def _predicate(driver: WebDriver):
        return title in driver.title

    return _predicate


def presence_of_element_located(locator: Tuple[str, str]) -> Callable[[WebDriverOrWebElement], WebElement]:
    """Ожидание для проверки того, что элемент присутствует в DOM страницы. ЭТО НЕ ОБЯЗАТЕЛЬНО ОЗНАЧАЕТ, ЧТО ЭЛЕМЕНТ ВИДЕН.
    locator - используется для поиска элемента 
    возвращает WebElement, когда он найден """

    def _predicate(driver: WebDriverOrWebElement):
        return driver.find_element(*locator)

    return _predicate


def url_contains(url: str) -> Callable[[WebDriver], bool]:
    """Ожидание для проверки того, что текущий url содержит подстроку, чувствительную к регистру.
    url - ожидаемый фрагмент url, возвращает True, если url совпадает, False в противном случае"""

    def _predicate(driver: WebDriver):
        return url in driver.current_url

    return _predicate


def url_matches(pattern: str) -> Callable[[WebDriver], bool]:
    """Ожидание для проверки текущего url.
    pattern - ожидаемый шаблон.
    Находит первое вхождение шаблона в текущем url и не требует точного полного совпадения. """

    def _predicate(driver: WebDriver):
        return re.search(pattern, driver.current_url) is not None

    return _predicate


def url_to_be(url: str) -> Callable[[WebDriver], bool]:
    """ Ожидание для проверки текущего url.
        url - ожидаемый url, который должен быть точным совпадением, 
        возвращает True, если url совпадает, false в противном случае."""

    def _predicate(driver: WebDriver):
        return url == driver.current_url

    return _predicate


def url_changes(url: str) -> Callable[[WebDriver], bool]:
    """ Ожидание для проверки текущего url.
        url - ожидаемый url, который не должен быть точным совпадением. 
        возвращает True, если url отличается, false - в противном случае."""

    def _predicate(driver: WebDriver):
        return url != driver.current_url

    return _predicate


def visibility_of_element_located(
    locator: Tuple[str, str]
) -> Callable[[WebDriverOrWebElement], Union[Literal[False], WebElement]]:
    """ Ожидание для проверки того, что элемент присутствует в DOM страницы и ВИДЕН. 
        Видимость означает, что элемент не только отображается, но и имеет высоту и ширину, которые больше 0.
        
        locator - используется для поиска элемента
        возвращает WebElement, если он найден и виден"""

    def _predicate(driver: WebDriverOrWebElement):
        try:
            return _element_if_visible(driver.find_element(*locator))
        except StaleElementReferenceException:
            return False

    return _predicate


def visibility_of(element: WebElement) -> Callable[[Any], Union[Literal[False], WebElement]]:
    """ Ожидание для проверки того, что элемент, о котором известно, что он присутствует в DOM страницы, является видимым.
        Видимость означает, что элемент не только отображается, но и имеет высоту и ширину, которые больше 0. 
        
        element - WebElement
        возвращает (тот же самый) WebElement, если он виден"""

    def _predicate(_):
        return _element_if_visible(element)

    return _predicate


def _element_if_visible(element: WebElement, visibility: bool = True) -> Union[Literal[False], WebElement]:
    return element if element.is_displayed() == visibility else False


def presence_of_all_elements_located(locator: Tuple[str, str]) -> Callable[[WebDriverOrWebElement], List[WebElement]]:
    """An expectation for checking that there is at least one element present on a web page.
locator is used to find the element returns the list of WebElements once they are located"""

    def _predicate(driver: WebDriverOrWebElement):
        return driver.find_elements(*locator)

    return _predicate


def visibility_of_any_elements_located(locator: Tuple[str, str]) -> Callable[[WebDriverOrWebElement], List[WebElement]]:
    """ Ожидание для проверки того, что на веб-странице виден хотя бы один элемент.
        
        locator используется для поиска элемента 
        возвращает список веб-элементов, когда они найдены
"""

    def _predicate(driver: WebDriverOrWebElement):
        return [element for element in driver.find_elements(*locator) if _element_if_visible(element)]

    return _predicate


def visibility_of_all_elements_located(
    locator: Tuple[str, str]
) -> Callable[[WebDriverOrWebElement], Union[List[WebElement], Literal[False]]]:
    """ Ожидание для проверки того, что все элементы присутствуют в DOM страницы и видны. 
        Видимость означает, что элементы не только отображаются, но и имеют высоту и ширину больше 0.
        
        locator - используется для поиска элементов
        возвращает список WebElements, когда они найдены и видны"""

    def _predicate(driver: WebDriverOrWebElement):
        try:
            elements = driver.find_elements(*locator)
            for element in elements:
                if _element_if_visible(element, visibility=False):
                    return False
            return elements
        except StaleElementReferenceException:
            return False

    return _predicate


def text_to_be_present_in_element(locator: Tuple[str, str], text_: str) -> Callable[[WebDriverOrWebElement], bool]:
    """ Ожидание для проверки наличия заданного текста в указанном элементе.
        
        locator, text
    """

    def _predicate(driver: WebDriverOrWebElement):
        try:
            element_text = driver.find_element(*locator).text
            return text_ in element_text
        except StaleElementReferenceException:
            return False

    return _predicate


def text_to_be_present_in_element_value(
    locator: Tuple[str, str], text_: str
) -> Callable[[WebDriverOrWebElement], bool]:
    """ Ожидание для проверки наличия заданного текста в ЗНАЧЕНИИ элемента.
        
        locator, text
"""

    def _predicate(driver: WebDriverOrWebElement):
        try:
            element_text = driver.find_element(*locator).get_attribute("value")
            return text_ in element_text
        except StaleElementReferenceException:
            return False

    return _predicate


def text_to_be_present_in_element_attribute(
    locator: Tuple[str, str], attribute_: str, text_: str
) -> Callable[[WebDriverOrWebElement], bool]:
    """ Ожидание для проверки наличия заданного текста В АТРИБУТЕ элемента.
        
        locator, attribute, text
    """

    def _predicate(driver: WebDriverOrWebElement):
        try:
            element_text = driver.find_element(*locator).get_attribute(attribute_)
            if element_text is None:
                return False
            return text_ in element_text
        except StaleElementReferenceException:
            return False

    return _predicate


def frame_to_be_available_and_switch_to_it(locator: Union[Tuple[str, str], str]) -> Callable[[WebDriver], bool]:
    """ Ожидание для проверки того, доступен ли заданный фрейм для переключения.
        Если фрейм доступен, он переключает данный драйвер на указанный фрейм."""

    def _predicate(driver: WebDriver):
        try:
            if isinstance(locator, Iterable) and not isinstance(locator, str):
                driver.switch_to.frame(driver.find_element(*locator))
            else:
                driver.switch_to.frame(locator)
            return True
        except NoSuchFrameException:
            return False

    return _predicate


def invisibility_of_element_located(
    locator: Union[WebElement, Tuple[str, str]]
) -> Callable[[WebDriverOrWebElement], Union[WebElement, bool]]:
    """ Ожидание для проверки того, что элемент либо невидим, либо отсутствует в DOM.
        locator, используется для поиска элемента"""

    def _predicate(driver: WebDriverOrWebElement):
        try:
            target = locator
            if not isinstance(target, WebElement):
                target = driver.find_element(*target)
            return _element_if_visible(target, visibility=False)
        except (NoSuchElementException, StaleElementReferenceException):
            # В случае NoSuchElement возвращается true, потому что элемент отсутствует в DOM. 
            # Блок try проверяет, присутствует ли элемент, но является невидимым. 
            # В случае StaleElementReference возвращается true, поскольку устаревшая ссылка
            # на элемент подразумевает, что элемент больше не виден.
            return True

    return _predicate


def invisibility_of_element(
    element: Union[WebElement, Tuple[str, str]]
) -> Callable[[WebDriverOrWebElement], Union[WebElement, bool]]:
    """ Ожидание для проверки того, что элемент либо невидим, либо отсутствует в DOM.
        
        element - это либо locator (текст), либо WebElement
    """
    return invisibility_of_element_located(element)


def element_to_be_clickable(
    mark: Union[WebElement, Tuple[str, str]]
) -> Callable[[WebDriverOrWebElement], Union[Literal[False], WebElement]]:
    """ Ожидание для проверки того, что элемент виден и включен так, что его можно щелкнуть.
        
        element - это либо locator (текст), либо WebElement
    """

    # Переименовали аргумент в 'mark', чтобы указать, что оба аргумента - locator и WebElement - являются допустимыми
    def _predicate(driver: WebDriverOrWebElement):
        target = mark
        if not isinstance(target, WebElement):  # если вместо WebElement задан locator
            target = driver.find_element(*target)  # захватить элемент в locator
        element = visibility_of(target)(driver)
        if element and element.is_enabled():
            return element
        return False

    return _predicate


def staleness_of(element: WebElement) -> Callable[[Any], bool]:
    """Подождите, пока элемент не перестанет быть подключенным(attached) к DOM.

    element - элемент, который нужно дождаться. возвращает False, если элемент
    все еще прикреплен к DOM, true - в противном случае.
    """

    def _predicate(_):
        try:
            # Вызов любого метода заставляет проверить его на состояние стабильности
            element.is_enabled()
            return False
        except StaleElementReferenceException:
            return True

    return _predicate


def element_to_be_selected(element: WebElement) -> Callable[[Any], bool]:
    """ Ожидание для проверки того, что объект выбран.

        элемент - объект WebElement
    """

    def _predicate(_):
        return element.is_selected()

    return _predicate


def element_located_to_be_selected(locator: Tuple[str, str]) -> Callable[[WebDriverOrWebElement], bool]:
    """ Выбирается ожидание для элемента, который должен быть обнаружен.

        locator - кортеж из (by, path)
    """

    def _predicate(driver: WebDriverOrWebElement):
        return driver.find_element(*locator).is_selected()

    return _predicate


def element_selection_state_to_be(element: WebElement, is_selected: bool) -> Callable[[Any], bool]:
    """Ожидание для проверки того, выбран ли данный элемент.

    элемент - WebElement 
    объект is_selected - логическое значение.
    """

    def _predicate(_):
        return element.is_selected() == is_selected

    return _predicate


def element_located_selection_state_to_be(
    locator: Tuple[str, str], is_selected: bool
) -> Callable[[WebDriverOrWebElement], bool]:
    """Ожидание для определения местоположения элемента и проверки, находится ли он в указанном состоянии выбора.

    locator - кортеж из (by, path). 
    is_selected - логическое значение
    """

    def _predicate(driver: WebDriverOrWebElement):
        try:
            element = driver.find_element(*locator)
            return element.is_selected() == is_selected
        except StaleElementReferenceException:
            return False

    return _predicate


def number_of_windows_to_be(num_windows: int) -> Callable[[WebDriver], bool]:
    """ Ожидание того, что количество окон будет иметь определенное значение."""

    def _predicate(driver: WebDriver):
        return len(driver.window_handles) == num_windows

    return _predicate


def new_window_is_opened(current_handles: List[str]) -> Callable[[WebDriver], bool]:
    """ 
    An expectation that a new window will be opened and have the number of windows handles increase.
    Ожидание того, что будет открыто новое окно и увеличится количество оконных манипуляторов."""

    def _predicate(driver: WebDriver):
        return len(driver.window_handles) > len(current_handles)

    return _predicate


def alert_is_present() -> Callable[[WebDriver], Union[Alert, Literal[False]]]:
    """Ожидание для проверки наличия оповещения и переключения на него."""

    def _predicate(driver: WebDriver):
        try:
            return driver.switch_to.alert
        except NoAlertPresentException:
            return False

    return _predicate


def element_attribute_to_include(locator: Tuple[str, str], attribute_: str) -> Callable[[WebDriverOrWebElement], bool]:
    """Ожидание для проверки того, включен ли заданный атрибут в указанный элемент.

    locator, attribute
    """

    def _predicate(driver: WebDriverOrWebElement):
        try:
            element_attribute = driver.find_element(*locator).get_attribute(attribute_)
            return element_attribute is not None
        except StaleElementReferenceException:
            return False

    return _predicate


def any_of(*expected_conditions: Callable[[D], T]) -> Callable[[D], Union[Literal[False], T]]:
    """ Ожидание того, что любое из нескольких предполагаемых условий будет истинным.
        
        Эквивалентно логическому 'ИЛИ'. 
        Возвращает результат первого совпадающего условия или False, если ни одно из них не выполняется.
    """

    def any_of_condition(driver: D):
        for expected_condition in expected_conditions:
            try:
                result = expected_condition(driver)
                if result:
                    return result
            except WebDriverException:
                pass
        return False

    return any_of_condition


def all_of(
    *expected_conditions: Callable[[D], Union[T, Literal[False]]]
) -> Callable[[D], Union[List[T], Literal[False]]]:
    """ Ожидание того, что все несколько ожидаемых условий будут истинными.

        Эквивалентно логическому 'AND'.
        Возвращает: Если какое-либо из ожидаемых условий не выполнено: False.
        Когда все ожидаемые условия выполнены: Список с возвращаемым значением каждого ожидаемого условия.
    """

    def all_of_condition(driver: D):
        results: List[T] = []
        for expected_condition in expected_conditions:
            try:
                result = expected_condition(driver)
                if not result:
                    return False
                results.append(result)
            except WebDriverException:
                return False
        return results

    return all_of_condition


def none_of(*expected_conditions: Callable[[D], Any]) -> Callable[[D], bool]:
    """ Ожидание того, что ни одно из 1 или нескольких ожидаемых условий не является истинным.

        Эквивалентно логическому 'NOT-OR'. 
        Возвращает логическое значение
    """

    def none_of_condition(driver: D):
        for expected_condition in expected_conditions:
            try:
                result = expected_condition(driver)
                if result:
                    return False
            except WebDriverException:
                pass
        return True

    return none_of_condition
