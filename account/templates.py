EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>Document</title>
  </head>
  <body>
    <form
      style="display: table; margin: 4rem auto;"
      method="POST"
      action="http://10.58.7.96:8000/accounts/auth-success/${Token}/"
    >
      <img
        src="http://byeol.dothome.co.kr/img/fixo_ko2.png"
        alt="logo"
        width="90"
        style="margin-bottom: 1rem;"
      />
      <div style="border: 1px solid #b3b3b3; width: 30rem; padding: 4rem 5rem;">
        <h4
          style="
            font-size: 1.2rem;
            color: #7903d4;
            margin: 0;
            font-weight: 900;
          "
        >
          Corrector Certification
        </h4>
        <h2 style="font-size: 2.2rem; margin: 0 0 1rem;color:#222">
          현직자 인증 확인
        </h2>
        <p style="font-size: 1rem; line-height: 1.5rem; margin: 2rem 0 2rem;color:#222">
          <strong
            >안녕하세요.
            <strong style="color: #7903d4;">픽소서</strong>입니다.</strong
          ><br /><br />
          국내 최대 자소서 첨삭사이트 픽소서에 가입해 주셔서 감사합니다.<br /><br />
          아래 버튼을 눌러 인증을 완료해주세요.<br />
          인증 버튼을 누르시면 첨삭자 인증이 완료되며, 픽소서 사이트로
          연결됩니다.
        </p>
        <button
          style="
            display: inline-block;
            text-decoration: none;
            padding: 20px 30px;
            border-radius: 14px;
            border: none;
            background: #7903d4;
            box-shadow: 4px 4px 6px #a2a2a2;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
          "
          rel="noreferrer noopener"
          target="_blank"
          href="http://10.58.5.155:8000/accounts/auth-success/${Token}/"
        >
          현직자 인증하기
        </button>
        <p
          style="
            font-size: 0.8rem;
            color: #8e8e8e;
            text-align: center;
            border-top: 1px solid #b3b3b3;
            padding-top: 2rem;
            margin-top: 4rem;
          "
        >
          대표번호:010-3725-7637 | EMAIL :
          <a
            href="mailto:${From}"
            style="
              color: #8e8e8e;
              text-decoration: none !important;
              font-size: 0.8rem;
            "
            >${From}</a
          >
        </p>
      </div>
    </form>
  </body>
</html>
"""