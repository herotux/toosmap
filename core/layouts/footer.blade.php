<div class="container-fluid new-letter">
    <div class="container">
        <div class="row">
            <div class="col-lg-2 col-md-2 hidden-sm hidden-xs">
            </div>
            <div class="col-lg-8 col-md-8 col-sm-12 col-xs-12">
                <div class="newsletter">

                    <table class="form">
                        <tbody>
                        <tr>
                            <td class="caption">از آخرین خبر ‌های ما مطلع باشید</td>
                            <td class="email-box">
                                <input id="user_email"  class="inputbox" name="user[email]" placeholder="ایمیل" type="text">

                            </td>
                            <td class="buttons">
                                <input class="button subbutton btn btn-primary" value="عضویت" name="Submit"
                                       type="submit">
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="col-lg-2 col-md-2 hidden-sm hidden-xs">
            </div>
        </div>
    </div>
</div>
<div class="container-fluid footer">
    <div class="container gap-col">
        <div class="row">
            <div class="col-sm-3 col-sm-6 col-1">
                <h3 class="footer-title">تماس با ما</h3>
                @if($site_settings['address'])
                    <p class="address">
                        <i class="icon"></i>
                        <span class="txt-info">
                          <span class="caption-f">نشانی دفتر:</span>
                          <span>{{ $site_settings['address'] }}</span>
                        </span>
                    </p>
                @endif
                @if($site_settings['tel'])
                    <p class="cal-footer">
                        <i class="icon"></i>
                        <span class="txt-info">
                         <span class="caption-f">روابط عمومی:</span>
                         <span class="cal-footer">{{ $site_settings['tel'] }}</span>
                        </span>
                    </p>
                @endif
                @if($site_settings['email'])
                    <p class="mil">
                        <i class="icon"></i>
                        <span class="caption-f">: پست الکترونیک:</span>
                        <span><a href="mailto:{{ $site_settings['email'] }}">{{ $site_settings['email'] }}</a></span>
                    </p>
                @endif
                @if($site_settings['fax'])
                    <p class="fax">
                        <i class="icon"></i>
                        <span class="txt-info">
                          <span class="caption-f">دورنگار:</span>
                          <span class="cal-footer">{{ $site_settings['fax'] }}</span>
                        </span>
                    </p>
                @endif
            </div>
            <div class="col-sm-3 col-sm-6 col2">
                <h3 class="footer-title">دسترسی سریع</h3>
                <ul class="lnk-footer">
                    <li><a href="#">پروسه  خرید چگونه است ؟</a></li>
                </ul>
            </div>
            <div class="col-sm-3 col-sm-6 col-3">
                <h3 class="footer-title">پیگیری سفارشات و ارسال</h3>
                <ul class="lnk-footer send-method">
                    <li><a href="#">زمان رسیدن محصول </a></li>
                    <li><a href="#">روش های ارسال و دریافت</a></li>

                </ul>
                <ul class="lnk-footer">
                    <li><a href="#">چگونه مقایسه کنم ؟</a></li>
                    <li><a href="#">پروسه خرید چگونه است ؟</a></li>
                    <li><a href="#">چگونه اعتماد کنم ؟</a></li>
                </ul>
            </div>
            <div class="col-sm-3 col-sm-6 col-4">
                <h3 class="footer-title">مجوزها </h3>
                <ul class="namad">
                    <li><img src="/images/namad/namad.png" class="img-responsive"></li>
                    <li><img src="/images/namad/samaneh.png" class="img-responsive"></li>
                </ul>
            </div>

        </div>
        <div class="row row-bottom">
            <div class="col-sm-4 col-xs-12 col-1 sotial-footer">
                <span>با ما همراه باشید</span>
                <ul>
                    @if($site_settings['google'])
                        <li>
                            <a class="google" href="{{ $site_settings['google'] }}">
                                <span class="flip"><img src="/images/social/Instagram.png"/></span>
                                <span class="flop"><img src="/images/social/Instagram.png"/></span>
                            </a>
                        </li>
                    @endif
                    @if($site_settings['telegram'])
                        <li>
                            <a class="tw" href="{{ $site_settings['telegram'] }}">
                                <span class="flip"><img src="/images/social/Telegram.png"/></span>
                                <span class="flop"><img src="/images/social/Telegram.png"/></span>
                            </a>
                        </li>
                    @endif
                    @if($site_settings['twitter'])
                        <li>
                            <a class="ins" href="{{ $site_settings['twitter'] }}">
                                <span class="flip"><img src="/images/social/twitter.png"/></span>
                                <span class="flop"><img src="/images/social/twitter.png"/></span>
                            </a>
                        </li>
                    @endif
                    @if($site_settings['facebook'])
                        <li>
                            <a class="video" href="{{ $site_settings['facebook'] }}">
                                <span class="flip"><img src="/images/social/Facebook.png"/></span>
                                <span class="flop"><img src="/images/social/Facebook.png"/></span>
                            </a>
                        </li>
                    @endif
                    @if($site_settings['facebook'])
                        <li>
                            <a class="video" href="{{ $site_settings['facebook'] }}">
                                <span class="flip"><img src="/images/social/Facebook.png"/></span>
                                <span class="flop"><img src="/images/social/Facebook.png"/></span>
                            </a>
                        </li>
                    @endif
                </ul>
            </div>
            <div class="col-sm-8 col-xs-12 gap-col">
                <div class="row">
                    <div class="col-sm-5 col-xs-12 gap-col">
                        <ul class="app">
                            <li><a href="#"><img src="/images/social/bazar.png" class="img-responsive"/></a></li>
                            <li><a href="#"><img src="/images/social/ios.png" class="img-responsive"/></a></li>
                        </ul>
                    </div>
                    <div class="col-sm-7 hidden-xs gap-col">
                        <ul class="menu-footer">
                            <li><a href="#">درباره ما</a></li>
                            <li><a href="#">تماس با ما</a></li>
                            <li><a href="#">سوالات متداول</a></li>
                            <li><a href="#">گالری</a></li>
                            <li><a href="#">سفارشات خاص</a></li>
                            <li><a href="#">آموزش</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="container-fluid copy">
    <div class="container gap-col">
        <div class="col-sm-6 col-xs-12 gap-col company">
            <p>تمامی حقوق محفوظ است</p>
        </div>
        <div class="col-sm-6 col-xs-12 gap-col npco">
            <a href="#">قدرت گرفته از ...</a>
        </div>
    </div>
</div>
</div>
</div>