let sector, tag, market

function radio(keyword, index) {
    return `<div class="form-check">
            <input class="form-check-input" value=${index} type="radio" name="flexRadioDefault" id="flexRadioDefault1">
            <label class="form-check-label" for="flexRadioDefault1">
            ${keyword}</label></div>`
}

function info_btn(company) {
    return `<li>${company.name}<button
            type="button"
            onclick='info_alert("${company.name}")'
            class="btn btn-outline-warning">정보</button></li>`
}

function sel0() {
    $("#stocks").empty()
    $("#stocks").append(radio('코스피', 1))
    $("#stocks").append(radio('코스닥', 2))
    $("#push0").toggleClass('is-hidden')
    $("#push1").toggleClass('is-hidden')
}

function sel1() {
    market = $("#flexRadioDefault1:checked").val()
    $("#stocks").empty()
    $("#stocks").append(radio('반도체와반도체장비', 1))
    $("#stocks").append(radio('양방향미디어와서비스', 2))
    $("#stocks").append(radio('자동차', 3))
    $("#push1").toggleClass('is-hidden')
    $("#push2").toggleClass('is-hidden')
}

function sel2() {
    sector = $("#flexRadioDefault1:checked").val()
    $("#stocks").empty()
    $("#stocks").append(radio('메모리', 1))
    $("#stocks").append(radio('플랫폼', 2))
    $("#stocks").append(radio('전기차', 4))
    $("#push2").toggleClass('is-hidden')
    $("#push3").toggleClass('is-hidden')
}

function sel3() {
    tag = $("#flexRadioDefault1:checked").val()
    $("#stocks").empty()
    $("#push3").toggleClass('is-hidden')
    $("#push4").toggleClass('is-hidden')
    $.ajax({
        type: "POST",
        url: '/stock',
        data: {
            tag: tag,
            market: market,
            sector: sector,
        },
        success: function (response) {
            let result = response['result']

            for (let i = 0; i < result.length; i++) {
                $("#stocks").append(info_btn(result[i]))
                $.cookie(`${result[i].name}`, JSON.stringify(result[i]))
            }
        }
    })
}

function ref() {
    location.reload()
}

function info_alert(name) {
    let json = $.cookie(name)
    let company = JSON.parse(json)
    let {price, capitalization, PER} = company
    window.alert(`
            주가: ${price}
            시가 총액: ${capitalization}
            PER: ${PER}`)
}