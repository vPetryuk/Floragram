console.log('hello world')
const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirm-btn')
const input = document.getElementById('id_avatar')
const avatar = document.getElementById('profile_avatar')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const first_name = document.getElementById('id_first_name')
const last_name = document.getElementById('id_first_name')
const bio = document.getElementById('id_bio')

input.addEventListener('change', ()=>{
    alertBox.innerHTML = ""
    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)

    imageBox.innerHTML = `<img src="${url}" id="image" width="700px">`
    var $image = $('#image')
    console.log($image)

    $image.cropper({
        aspectRatio: 9 / 9,
        crop: function(event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
        }
    });



    var cropper = $image.data('cropper');
    confirmBtn.addEventListener('click', ()=>{
        console.log('buttonclick');
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed')
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrf[0].value)
            fd.append('avatar', blob, 'my-image.png');
            fd.append('first_name',first_name.value)
            fd.append('last_name',last_name.value)
            fd.append('bio',bio.value)
            console.log(fd);
            $.ajax({
                type:'POST',
                url: imageForm.action,
                enctype: 'multipart/form-data',
                data: fd,
                success: function(response){
                    location.reload();
                    console.log('success', response)
                    alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                            Successfully saved and cropped the selected image
                                        </div>`
                },
                error: function(error){
                    console.log('error', error)
                    alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                            Ups...something went wrong
                                        </div>`
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        })
    })

})

 confirmBtn.addEventListener('click', ()=>{
        console.log('buttonclick2');
        const fd = new FormData();
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        fd.append('first_name',first_name.value)
        fd.append('last_name',last_name.value)
        fd.append('bio',bio.value)
        console.log(fd);
        $.ajax({
            type:'POST',
            url: imageForm.action,
            enctype: 'multipart/form-data',
            data: fd,
            success: function(response){
                location.reload();
                console.log('success', response)
                alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                            Successfully saved and cropped the selected image
                                        </div>`
            },
            error: function(error){
                console.log('error', error)
                alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                            Ups...something went wrong
                                        </div>`
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    })
