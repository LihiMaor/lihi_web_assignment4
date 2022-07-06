function FrontedFunc() {
    var frontend_form = document.getElementById("frontedForm");
    var idInput = frontend_form.elements[0].value
    let element = document.createElement('a');
    element.href = 'https://reqres.in/api/users';
    element.pathname = element.pathname + '/' + idInput;
    fetch(element.href).then(
        response => response.json()
    ).then(
        responseOBJECT => createUsersList(responseOBJECT.data)
    ).catch(
        err => console.log(err)
    );
}









function createUsersList(response){
    const currMain = document.querySelector("main")
    const section = document.createElement('section')
    section.innerHTML = `
       <figure>
        <img src="${response.avatar}" alt="Profile Picture" width="100%"/>
        <figcaption>
            <p style=" font-size: 25px;  text-shadow: 2px 2px lightsalmon;   word-wrap: break-word;"> ${response.first_name} ${response.last_name}</p>
            <p > email: ${response.email} </p>
            <a href="mailto:${response.email}">Send Email</a>
        </figcaption>
    </figure>
        `
        currMain.appendChild(section)
        currMain.replaceChild(section, currMain.childNodes[0]);
}


