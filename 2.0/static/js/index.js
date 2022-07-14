window.onload = function(){
	const form = document.getElementById("form-login")

	form.addEventListener("submit", (ev)=>{
		ev.preventDefault()
		data = {
			email: document.getElementById("email").value,
			password: document.getElementById("password").value
		}
		fetch("/login",{
			method:"POST",
			body:JSON.stringify(data),
			headers:{
				'Content-Type':'application/json'
			}
		})
			.then(response => response.json())
			.then(data=>{
				if(data.status == 200){
					console.log(data)
					window.location.href = "/sale"
				}
				else{
					alert(data.message)
				}
			})
	})
}
