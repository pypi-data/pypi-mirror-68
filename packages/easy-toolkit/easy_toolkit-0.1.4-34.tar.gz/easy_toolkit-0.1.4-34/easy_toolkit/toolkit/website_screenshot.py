import os
import asyncclick as click
from pyppeteer import launch
from easy_toolkit.utils import current_dir, MeasuredEventLoop
from easy_toolkit.default_settings import SettingsHandler
import asyncio


@click.command(name="screenshot")
@click.option("-u", '--url', required=True, help="The target url.")
@click.option("-w", "--width", default=1920, help="The width of web page.")
@click.option("-p", "--path", default=current_dir(), help="Path to save image.")
@click.option("-n", "--name", default="", help="Image name.")
async def screenshot(url, width, path, name):
    # loop = asyncio.get_event_loop()
    loop = MeasuredEventLoop()
    asyncio.set_event_loop(loop)

    async def realrun(aname):
        executable_path = SettingsHandler.read_property("chrome_path")
        launch_args = {}
        if executable_path:
            click.echo(click.style(text="User customer chrome.exe: {}", fg="green").format(executable_path))
            launch_args.update({"executablePath": executable_path})
        else:
            click.echo(click.style(text="Tips: You can set [chrome_path] to assign your chrome.exe", fg='green'))
        browser = await launch(headless=True, args=launch_args)
        page = await browser.newPage()
        await page.setViewport({"width": width, "height": 1080})
        await page.goto(url, waitUntil="domcontentloaded")
        if not aname:
            aname = await page.title() + ".png"
        img_path = os.path.join(path, aname)
        click.echo("save file to: {}".format(img_path))
        await page.screenshot({'path': img_path, "fullPage": True}, )
        await browser.close()

    loop.run_until_complete(realrun(name))
    loop.close()
