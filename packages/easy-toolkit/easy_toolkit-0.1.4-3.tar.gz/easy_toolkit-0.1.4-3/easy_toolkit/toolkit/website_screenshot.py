import os
import asyncclick as click
from pyppeteer import launch
from easy_toolkit.utils import screen_size, current_dir, MeasuredEventLoop
import asyncio

ssize = screen_size()


@click.command(name="screenshot")
@click.option("-u", '--url', required=True, help="The target url.")
@click.option("-w", "--width", default=ssize[0], help="The width of web page.")
@click.option("-p", "--path", default=current_dir(), help="Path to save image.")
@click.option("-n", "--name", default="", help="Image name.")
async def screenshot(url, width, path, name):
    # loop = asyncio.get_event_loop()
    # print(type(loop), loop)
    loop = MeasuredEventLoop()
    asyncio.set_event_loop(loop)

    async def realrun(aname):
        browser = await launch()
        page = await browser.newPage()
        await page.setViewport({"width": width, "height": ssize[-1]})
        await page.goto(url, waitUntil="domcontentloaded")
        if not aname:
            aname = await page.title() + ".png"
        img_path = os.path.join(path, aname)
        click.echo("save file to: {}".format(img_path))
        await page.screenshot({'path': img_path, "fullPage": True}, )
        await browser.close()

    loop.run_until_complete(realrun(name))
    loop.close()
