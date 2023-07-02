( () => {
    'use strict'
    const uriCapture = `v1/video_capture`;
    const videoCapture = document.querySelector('#videoCapture');
    const photoCaptured = document.querySelector('#photoCaptured');
    
    
    const asycData = async(uri, method, type, formData = null ) => {
        let result = '', params = {}
        // document.querySelector(`#spinnerGrid`).removeAttribute('style')
        if( method == 'GET' ) {
            params = {
                method: "GET",
                redirect: "follow",
                headers: {
                    pragma: 'no-cache',
                    cache: 'reload',
                    'Cache-Control': 'no-cache',
                },
            };
        } else if (method == "POST") {
            params = {
                method: "POST",
                body: formData,
                headers: {
                    // 'Content-Type': 'application/json',
                    pragma: 'no-cache',
                    cache: 'reload',
                    'Cache-Control': 'no-cache',
                },
            };
        } else if (method == "DELETE") {
            params = {
                method: "DELETE",
                body: formData,
                headers: {
                    // 'Content-Type': 'application/json',
                    pragma: 'no-cache',
                    cache: 'reload',
                    'Cache-Control': 'no-cache',
                },
            };
        }
    
        const response = await fetch(uri, params);
        if (type == "json") result = await response.json();
        else result = await response.text();
        return result;
    };
    /** Obtenemos el Base64 de la imagen capturada */
    const getBase64Image = img => {
        const canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        const dataURL = canvas.toDataURL();
        return dataURL;
    }
    /** Inciamos el proceso de captura
     * abrimos la camara del usuario para tomar la foto
     */
    const btnStart = document.querySelector('#btnStart');
    btnStart.addEventListener('click', e => {
        asycData('/v1/start', 'POST', 'json', [] )
        .then( response => {
            // console.info(response);
            // videoCapture.setAttribute('height', '410px')
            videoCapture.src = uriCapture;
            photoCaptured.src = ''
            // const btnRestart = document.querySelector(`#btnRestart`);
            // btnRestart.classList.remove('hidden')
            btnStart.style.visibility = 'hidden';
            if( localStorage.getItem('capture') ) localStorage.removeItem('capture');
        })
        .catch( error => {
            console.log(error);
            Swal.fire({
                icon: 'error',
                title: 'Error al inicar la captura',
                text: 'Verifique que haya permitido el acceso a la cámara y vulva a iniciar el proceso',
            })
        })
    });
    /** Proceso de captura de imagen
     * Tomamos la foto y cerramos la camara si se detecta un
     * rostro, de lo contrario, se sigue capturando la imagen
     */
    const btnCapture = document.querySelector('#btnCapture')
    btnCapture.addEventListener('click', e => {
        // videoCapture.src = ''
        asycData('/v1/take-photos', 'POST', 'json', [])
        .then( response => {
            // console.info(response);
            const { status, path, photoName } = response;
            if( status ) {
                // photoCaptured.src = `${location.origin}/${path}${photoName}`
                photoCaptured.src = `${location.origin}/static/media/${photoName}`
                
                // videoCapture.setAttribute('height', 'auto')
                videoCapture.src = '';
                btnNoCapture.classList.remove('hidden');
                btnCheckCapture.classList.remove('hidden');
    
                // Detenemos la captura de video
                asycData('/v1/stop', 'GET', 'json')
                .then( resultStop => {
                    if(resultStop.status) {
                        console.info('Cámara a pagada');
                    }
                })
                .catch( error => {
                    console.log(error);
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al cerra la cámara',
                        text: 'la cámara no se ha podido cerrar.',
                    })
                })
            }
        })
        .catch( error => {
            console.log(error);
            Swal.fire({
                icon: 'error',
                title: 'Error al tomar la foto',
                text: 'Vuelva a inicar la cámara',
            })
            // Detenemos la captura de video
            asycData('/v1/stop', 'GET', 'json')
            .then( resultStop => {})
            .catch( error => {
                console.log(error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error al cerra la cámara',
                    text: 'la cámara no se ha podido cerrar.',
                })
            })
            
        })
    
    });
    
    // const btnRestart = document.querySelector('#btnRestart');
    // btnRestart.addEventListener('click', () => btnStart.click() );
    const btnNoCapture = document.querySelector('#btnNoCapture');
    btnNoCapture.addEventListener('click', () => {
        photoCaptured.src ='';
        btnNoCapture.classList.add('hidden');
        btnCheckCapture.classList.add('hidden');
        btnStart.click();
    } );
    const btnCheckCapture = document.querySelector('#btnCheckCapture');
    btnCheckCapture.addEventListener('click', () => {
        // btnRestart.classList.add('hidden');
        btnNoCapture.classList.add('hidden');
        btnCheckCapture.classList.add('hidden');
        btnStart.removeAttribute('style');

        // Verificamos que etiqueta IMG tenga la imagen
        // photoCaptured.onload = () => {
            // Obtenemos el base64 de la imagen
            const b64Img = getBase64Image(photoCaptured);
            // Almacenamos el base64 en una variable local
            localStorage.setItem('capture', b64Img);
        // };
    });
})()