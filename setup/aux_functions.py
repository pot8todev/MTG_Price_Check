from setup.driver_setup import driver


def hide_cookie():
    driver.execute_script(
        "document.getElementById('lgpd-cookie').style.display = 'none';"
    )
