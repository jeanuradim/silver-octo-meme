import base64
import random
import requests
from seleniumbase import SB

# -----------------------------
#  CONFIG & GEO
# -----------------------------
geo = requests.get("http://ip-api.com/json/").json()
latitude   = geo["lat"]
longitude  = geo["lon"]
timezone   = geo["timezone"]
proxy_str  = False

# Decode channel name
fulln = base64.b64decode("YnJ1dGFsbGVz").decode("utf-8")
urlt  = f"https://www.twitch.tv/{fulln}"


# -----------------------------
#  HELPERS
# -----------------------------
def click_if_exists(driver, selector, timeout=4):
    """Click element if present."""
    if driver.is_element_present(selector):
        driver.cdp.click(selector, timeout=timeout)


def prepare_stream(driver):
    """Handle cookies, start watching, etc."""
    click_if_exists(driver, 'button:contains("Accept")')
    driver.sleep(2)

    click_if_exists(driver, 'button:contains("Start Watching")')
    driver.sleep(2)

    click_if_exists(driver, 'button:contains("Accept")')
    driver.sleep(1)


def open_secondary_driver(parent, url):
    """Open a second stealth driver for extra watch time."""
    d2 = parent.get_new_driver(undetectable=True)
    d2.activate_cdp_mode(url, tzone=timezone, geoloc=(latitude, longitude))
    d2.sleep(10)
    prepare_stream(d2)
    return d2


# -----------------------------
#  MAIN LOOP
# -----------------------------
while True:
    with SB(
        uc=True,
        locale="en",
        ad_block=True,
        chromium_arg="--disable-webgl",
        proxy=proxy_str
    ) as nazarik:

        nazarik.activate_cdp_mode(urlt, tzone=timezone, geoloc=(latitude, longitude))
        nazarik.sleep(2)

        prepare_stream(nazarik)
        nazarik.sleep(10)

        # Check if stream is live
        if nazarik.is_element_present("#live-channel-stream-information"):

            # Open secondary viewer
            d2 = open_secondary_driver(nazarik, urlt)

            # Random watch time
            nazarik.sleep(random.randint(450, 800))

        else:
            print("Stream offline. Exiting loop.")
            break
