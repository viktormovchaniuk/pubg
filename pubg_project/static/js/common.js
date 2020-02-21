$(function() {
  $(".hamburger").click(function() {
    $(this).toggleClass("hamburger--active");
    $("nav").toggleClass("nav--active");
    $("header").toggleClass("header--menu");
  });

  $(".modal").popup({ transition: "all 0.3s" });

  $('input[type="tel"]').mask("+0 (000) 000-00-00");

  jQuery.validator.addMethod(
    "phoneno",
    function(phone_number, element) {
      return (
        this.optional(element) ||
        phone_number.match(
          /\+[0-9]{1}\s\([0-9]{3}\)\s[0-9]{3}-[0-9]{2}-[0-9]{2}/
        )
      );
    },
    "Введите Ваш телефон"
  );

  $(".form").each(function(index, el) {
    $(el).addClass("form-" + index);

    $(".form-" + index).validate({
      rules: {
        phone: {
          required: true,
          phoneno: true
        },
        name: "required"
      },
      messages: {
        name: "Введите Ваше имя",
        email: "Введите Ваш Email",
        content: "Введите Ваш вапрос"
      }
      // submitHandler: function(form) {
      //   var t = {
      //     name: jQuery(".form-" + index)
      //       .find("input[name=name]")
      //       .val(),
      //     email: jQuery(".form-" + index)
      //       .find("input[name=email]")
      //       .val(),
      //     content: jQuery(".form-" + index)
      //       .find("textarea[name=content]")
      //       .val(),
      //     subject: jQuery(".form-" + index)
      //       .find("input[name=subject]")
      //       .val()
      //   };
      //   ajaxSend(".form-" + index, t);
      // }
    });
  });

  // function ajaxSend(formName, data) {
  //   jQuery.ajax({
  //     type: "POST",
  //     url: "sendmail.php",
  //     data: data,
  //     success: function() {
  //       $(".modal").popup("hide");
  //       $("#thanks").popup("show");
  //       setTimeout(function() {
  //         $(formName).trigger("reset");
  //       }, 2000);
  //     }
  //   });
  // }

  $(window).scroll(function() {
    if ($(this).scrollTop() > 20) {
      $(".header").addClass("header--active");
    } else if ($(this).scrollTop() < 20) {
      $(".header").removeClass("header--active");
    }
  });

  if ($(this).scrollTop() > 20) {
    $(".header").addClass("header--active");
  }

  $(".header__list").on("click", "a", function(event) {
    event.preventDefault();
    var id = $(this).attr("href"),
      top = $(id).offset().top;
    $("body,html").animate({ scrollTop: top - 60 }, "slow", "swing");
  });

  $(".click").on("click", "a", function(event) {
    var id = $(this)
      .attr("href")
      .replace("/", "");

    if (id !== "#") {
      var top = $(id).offset().top;
      event.preventDefault();
      $("body,html").animate({ scrollTop: top - 60 }, 950);
    }
  });

  $(".tabs__wrap").hide();
  $(".tabs__wrap:first").show();
  $(".tabs ul a:first").addClass("active");
  $(".tabs ul a").click(function(event) {
    event.preventDefault();
    $(".tabs ul a").removeClass("active");
    $(this).addClass("active");
    $(".tabs__wrap").hide();
    var selectTab = $(this).attr("href");
    $(selectTab).fadeIn();
  });
});
