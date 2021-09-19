function sign_out() {
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃!')
    window.location.href = "/login"
}

function toggle_sign_up() {
    $("#btn-check-dup").toggleClass("is-hidden");
    $("#help-id").toggleClass("is-hidden");
    $("#sign-up-box").toggleClass("is-hidden");
    $("#div-sign-in-or-up").toggleClass("is-hidden");
    $("#help-password").toggleClass("is-hidden");
    $("#help-password2").toggleClass("is-hidden");
}

function is_nickname(asValue) {
    const regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    return regExp.test(asValue);
}

function is_password(asValue) {
    const regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return `${time.toFixed(0)}분 전`
    }
    time = time / 60  // 시간
    if (time < 24) {
        return `${time.toFixed(0)}시간 전`
    }
    time = time / 24
    if (time < 7) {
        return `${time.toFixed(0)}일 전`
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}
function num2str(count) {
    if (count > 5000) {
        return (count / 1000).toFixed(1) + "k"
    }
    if (count === 0) {
        return ""
    }
    return count
}

function check_dup() {
    let username = $("input#input-username").val();
    console.log(username);
    if (!(username)) {
        $("#help-id")
            .text("아이디를 입력해주세요.")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-username").focus();
        return;
    }
    if (!is_nickname(username)) {
        $("#help-id")
            .text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이")
            .removeClass("is-safe")
            .addClass("is-danger")
        $("#input-username").focus();
        return;
    }
    $("p#help-id").addClass("is-loading")
    $.ajax({
        type: "POST",
        url: "/sign_up/check_dup",
        data: {
            username_give: username
        },
        success: function (response) {
            if (response["exists"]) {
                $("#help-id")
                    .text("이미 존재하는 아이디입니다.")
                    .removeClass("is-safe")
                    .addClass("is-danger");
                $("#input-username").focus();
            } else {
                $("#help-id")
                    .text("사용할 수 있는 아이디입니다.")
                    .removeClass("is-danger")
                    .addClass("is-success");
            }
            $("p#help-id").removeClass("is-loading");
        }
    });
}

function sign_up() {
    let username = $("#input-username").val();
    let password = $("#input-password").val();
    let password2 = $("input#input-password2").val();
    console.log(username, password, password2);
    if ($("p#help-id").hasClass("is-danger")) {
        alert("아이디를 다시 확인해주세요.");
        return;
    } else if (!$("#help-id").hasClass("is-success")) {
        alert("아이디 중복확인을 해주세요.");
        return;
    }
    if (!(password)) {
        $("#help-password")
            .text("비밀번호를 입력해주세요.")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-password2").focus();
        return;
    } else if (!is_password(password)) {
        $("#help-password")
            .text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-password2").focus();
        return;
    } else {
        $("#help-password").text("사용할 수 있는 비밀번호입니다.")
            .removeClass("is-danger")
            .addClass("is-success");
    }
    if (!(password2)) {
        $("#help-password2").text("비밀번호 확인을 입력해주세요.")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-password2").focus();
        return;
    } else if (password2 !== password) {
        $("#help-password2")
            .text("비밀번호가 일치하지 않습니다.")
            .removeClass("is-safe")
            .addClass("is-danger");
        $("#input-password2").focus();
        return;
    } else {
        $("#help-password2")
            .text("비밀번호가 일치합니다.")
            .removeClass("is-danger")
            .addClass("is-success");
    }
    $.ajax({
        type: "POST",
        url: "/sign_up/save",
        data: {
            username_give: username,
            password_give: password
        },
        success: function () {
            alert("회원가입을 축하드립니다!")
            window.location.replace("/login")
        }
    });
}


function sign_in() {
    let username = $("input#input-username").val()
    let password = $("input#input-password").val()

    if (!(username)) {
        $("#help-id-login").text("아이디를 입력해주세요.")
        $("#input-username").focus()
        return;
    } else {
        $("#help-id-login").text("")
    }

    if (!(password)) {
        $("#help-password-login").text("비밀번호를 입력해주세요.")
        $("#input-password").focus()
        return;
    } else {
        $("#help-password-login").text("")
    }
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            username_give: username,
            password_give: password
        },
        success: function (response) {
            if (response['result'] === 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}

function update_profile() {
    let name = $('#input-name').val()
    let file = $('#input-pic')[0].files[0]
    let about = $("#textarea-about").val()
    let form_data = new FormData()
    form_data.append("file_give", file)
    form_data.append("name_give", name)
    form_data.append("about_give", about)
    console.log(name, file, about, form_data)

    $.ajax({
        type: "POST",
        url: "/update_profile",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] === "success") {
                alert(response["msg"])
                window.location.reload()
            }
        }
    });
}

function post() {
    let comment = $("#textarea-post").val()
    let today = new Date().toISOString()
    $.ajax({
        type: "POST",
        url: "/posting",
        data: {
            comment_give: comment,
            date_give: today
        },
        success: function () {
            $("#modal-post").removeClass("is-active")
            window.location.reload()
        }
    })
}
function get_posts(username) {
    if (username === undefined) {
        username = ""
    }
    $("#post-box").empty()
    $.ajax({
        type: "GET",
        url: `/get_posts?username=${username}`,
        data: {},
        success: function (response) {
            if (response["result"] === "success") {
                let posts = response["posts"]
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    console.log(post)
                    let time_post = new Date(post["date"])
                    let time_before = time2str(time_post)
                    let class_heart = post['heart_by_me'] ? "fa-heart": "fa-heart-o"
                    let class_star = post['star_by_me'] ? "fa-star": "fa-star-o"
                    let class_like = post['like_by_me'] ? "fa-thumbs-up" : "fa-thumbs-o-up"

                    let html_temp = `
                    <div class="box" id="${post["_id"]}">
                        <article class="media">
                            <div class="media-left">
                                <a class="image is-64x64" href="/user/${post['username']}">
                                    <img class="is-rounded" src="/static/profile_pics/profile_placeholder.png" alt="profile">
                                </a>
                            </div>
                            <div class="media-content">
                                <div class="content">
                                    <p>
                                        <strong>${post['profile_name']}</strong> <small>@${post['username']}</small> <small>${time_before}</small>
                                        <br>${post['comment']}
                                    </p>
                                </div>
                                <nav class="level is-mobile">
                                    <div class="level-left">
                                        <a class="level-item is-sparta" aria-label="heart" onclick="toggle_like('${post['_id']}', 'heart')">
                                            <span class="icon is-small">
                                            <i class="fa ${class_like}" aria-hidden="true"></i></span>&nbsp;<span class="like-num">${post["count_heart"]}</span>
                                        </a>
                                        <a class="level-item is-sparta" aria-label="star" onclick="toggle_like('${post['_id']}', 'star')">
                                            <span class="icon is-small">
                                            <i class="fa ${class_star}" aria-hidden="true"></i></span>&nbsp;<span class="like-num">${post["count_star"]}</span>
                                        </a>
                                        <a class="level-item is-sparta" aria-label="like" onclick="toggle_like('${post['_id']}', 'like')">
                                            <span class="icon is-small">
                                            <i class="fa ${class_like}" aria-hidden="true"></i></span>&nbsp;<span class="like-num">${post["count_like"]}</span>
                                        </a>
                                    </div>
                                </nav>
                            </div>
                        </article>
                    </div>`
                    $("#post-box").append(html_temp)
                }
            }
        }
    })
}

function toggle_like(post_id, type) {
    console.log(post_id, type)
    let $a_like = $(`#${post_id} a[aria-label='${type}']`)
    let $i_like = $a_like.find("i")
    let class_s = {"heart": "fa-heart", "star": "fa-star", "like": "fa-thumbs-up"}
    let class_o = {"heart": "fa-heart-o", "star": "fa-star-o", "like": "fa-thumbs-o-up"}
    if ($i_like.hasClass(class_s[type])) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass(class_o[type]).removeClass(class_s[type])
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass(class_s[type]).removeClass(class_o[type])
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })
    }
}
