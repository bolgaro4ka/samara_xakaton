const btn=document.getElementById("letsGoSearch")
const field=document.getElementsByName("searchField")[0]
btn.addEventListener("click", (e)=>{window.find(field.value); console.log(field.value)})