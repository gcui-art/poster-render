import pyppeteer
from fastapi import APIRouter, Response
from pydantic import BaseModel

from config import settings

router = APIRouter()


class PosterContent(BaseModel):
    content: str


@router.post("/generate")
async def generate_post(params: PosterContent):
    browser = await pyppeteer.launcher.connect(
        browserWSEndpoint=settings.browser.hostname
    )

    page = await browser.newPage()
    await page.setViewport({
        "width": 700,
        "height": 100,
    })

    html_string = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>gapier</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap">
        <meta charset="UTF-8" />
        <style>
          body {{
            margin: 0;
            padding: 0;
            font-family: 'Noto Sans SC', sans-serif;
          }}
          .time {{
            color: #f4f4f4;
            margin-bottom: 0;
            margin-top: 30px;
          }}
          .title {{
            color: #fff;
          }}
    
          .gradient-background {{
            // background: linear-gradient(to bottom, #b326b5, #eb4c5f);
            height: 100%s;
            // min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
          }}
    
          .content {{
            background-color: #fff;
            width: 80%;
            max-width: 600px;
            padding: 20px;
            // border-radius: 10px;
            border-radius: 1rem;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            color: #1e293b;
            height: 100%;
            // min-height: 80vh;
          }}

          .footer {{
            color: #f4f4f4;
          }}
          .footer a {{
            color: #f4f4f4;
          }}
        </style>
      </head>
      <body>
        <div class="gradient-background">
          <div class="content">
            {params.content}
          </div>
          <p class="footer">
            powered by gapier.com
          </p>
        </div>
      </body>
    </html>
    """
    # html_string = html_string % html_result
    await page.setContent(html_string)
    # await page.waitForFunction("document.fonts.ready.then(() => true)", {
    #     "timeout": 10000,
    # })
    content_height = await page.evaluate("""() => {
      const content = document.documentElement || document.body;
      return content.scrollHeight;
    }""")
    await page.setViewport({
        "width": 700,
        "height": content_height,
    })
    screenshot = await page.screenshot({"fullPage": True})
    await browser.close()

    return Response(content=screenshot, media_type="image/png")
