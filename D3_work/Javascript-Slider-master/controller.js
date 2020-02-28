var slideList = [   { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '1Welcome to Menucool Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-2.jpg', text : '2Customizable Transition Effects' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-3.jpg', text : '3The slide is a linking image' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-4.jpg', text : '4Pure Javascript. No jQuery. No flash.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-5.jpg', text : '5HTML caption. Back to Menucool.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '6Most light weight Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '7Welcome to Menucool Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-2.jpg', text : '8Customizable Transition Effects' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-3.jpg', text : '9The slide is a linking image' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-4.jpg', text : '10Pure Javascript. No jQuery. No flash.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-5.jpg', text : '11HTML caption. Back to Menucool.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '12Most light weight Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-3.jpg', text : '13The slide is a linking image' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-4.jpg', text : '14Pure Javascript. No jQuery. No flash.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-5.jpg', text : '15HTML caption. Back to Menucool.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '16Most light weight Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '17Welcome to Menucool Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-2.jpg', text : '18Customizable Transition Effects' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-3.jpg', text : '19The slide is a linking image' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-4.jpg', text : '20Pure Javascript. No jQuery. No flash.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-5.jpg', text : '21HTML caption. Back to Menucool.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '22Most light weight Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-3.jpg', text : '23The slide is a linking image' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-4.jpg', text : '24Pure Javascript. No jQuery. No flash.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-5.jpg', text : '25HTML caption. Back to Menucool.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '26Most light weight Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '27Welcome to Menucool Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-2.jpg', text : '28Customizable Transition Effects' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-3.jpg', text : '29The slide is a linking image' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-4.jpg', text : '30Pure Javascript. No jQuery. No flash.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-5.jpg', text : '31HTML caption. Back to Menucool.' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-1.jpg', text : '32Most light weight Image Slider' },
                    { imgUrl: 'http://www.menucool.com/slider/jsImgSlider/images/image-slider-2.jpg', text : '33Choose from multiple themes to suit your own style' } ]

var slideLen = slideList.length;
var cur = -1
var prev = 0
var timer = null
var config = { auto_play: true,
               slideTime: 3000,
               fadeInTime: 2000 }

function thumbListRight(){
    var leftPixel = document.getElementById("thumbnailList").style.left
    if(parseInt(leftPixel, 10) > ((slideLen-1)*(-80)+504) )
        $("#thumbnailList").animate({left: (parseInt(leftPixel, 10) - 504) + 'px'})
}

function thumbListLeft(){
    var leftPixel = document.getElementById("thumbnailList").style.left
    if(parseInt(leftPixel, 10) < 0)
        $("#thumbnailList").animate({left: (parseInt(leftPixel, 10) + 504) + 'px'})
}

function loadImages(){

    var thumbnailList = document.getElementById("thumbnailList")
    for(var i in slideList){

        var thumbnail = document.createElement("li")
        thumbnail.setAttribute("id", "thumb_frame_"+i)
        thumbnail.setAttribute("class", "thumb")

        var thumbImage = document.createElement("img")
        thumbImage.setAttribute("id", "thumb_"+i)
        thumbImage.setAttribute("src", slideList[i].imgUrl)
        thumbImage.setAttribute("text", slideList[i].text)

        thumbImage.addEventListener('mouseover', function(event) {
            event.target.style.opacity = "1"
        })
        thumbImage.addEventListener('mouseout', function(event) {
            event.target.style.opacity = "0.5"
        })
        thumbImage.addEventListener('click', function(event) {
            if(config.auto_play)
                clearInterval(timer)
            document.getElementById("mainImage").src = event.target.src
            document.getElementById("imageCaption").innerHTML = event.target.getAttribute("text")
            var img_id = event.target.getAttribute("id")
            document.getElementById("thumb_" + cur).style.opacity = "0.5"
            cur = Number(img_id.substring(img_id.indexOf("_")+1, img_id.length))
            document.getElementById("thumb_" + cur).style.opacity = "1"
            if(config.auto_play)
                slideIt()
        })
        thumbnail.appendChild(thumbImage)
        thumbnailList.appendChild(thumbnail)
    }
}

window.onload = function start(){
    loadImages()
    nextSlide()
    slideIt()
    $('#mainImage').on('load', function(){
        $('.spinner').hide()
    })

    $("#confBtn").click(function(){
        $("#configId").slideToggle(500, function(){

        })
    })
}

function slideIt(){
    timer = setInterval(nextSlide, config.slideTime)
}

function nextSlide(){
    prev = cur
    cur = (cur + 1) % slideLen
    if(cur != 0 && cur % 6 == 0)
        thumbListRight()

    var mainImage = document.getElementById("mainImage")
    mainImage.style.display = "none"
    mainImage.src = slideList[cur].imgUrl
    $("#mainImage").fadeIn(config.fadeInTime)
    document.getElementById("imageCaption").innerHTML = slideList[cur].text
    if(document.getElementById("thumb_" + prev))
        document.getElementById("thumb_" + prev).style.opacity = "0.5"
    document.getElementById("thumb_" + cur).style.opacity = "1"
    if(cur == 0)
        $("#thumbnailList").animate({left: '0px'})
}

function toggleAutoPlay(){
    if(config.auto_play == true){
        clearInterval(timer)
        config.auto_play = false
        document.getElementById("autoplayTime").disabled = true
    }else{
        config.auto_play = true
        slideIt()
        document.getElementById("autoplayTime").disabled = false
    }
}

function changeFadeIn(dom){
    config.fadeInTime = Number(dom.value)
}

function changeAutoplay(dom){
    clearInterval(timer)
    config.slideTime = Number(dom.value)
    slideIt()
}
