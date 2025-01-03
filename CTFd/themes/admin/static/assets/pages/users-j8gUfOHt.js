import{$ as e,e as a,C as l,A as u}from"./main-C4_GQfqy.js";function d(r){let t=e("input[data-user-id]:checked").map(function(){return e(this).data("user-id")}),s=t.length===1?"user":"users";a({title:"Delete Users",body:`Are you sure you want to delete ${t.length} ${s}?`,success:function(){const i=[];for(var o of t)i.push(l.fetch(`/api/v1/users/${o}`,{method:"DELETE"}));Promise.all(i).then(n=>{window.location.reload()})}})}function c(r){let t=e("input[data-user-id]:checked").map(function(){return e(this).data("user-id")});u({title:"Edit Users",body:e(` 
    <form id="users-bulk-edit">
      <div id="Verified" class="form-group Verified">
        <label>Verified</label>
        <select name="verified" data-initial="">
          <option value="">--</option>
          <option value="true">True</option>
          <option value="false">False</option>
        </select>
      </div>
      <div class="form-group">
        <label>Banned</label>
        <select name="banned" data-initial="">
          <option value="">--</option>
          <option value="true">True</option>
          <option value="false">False</option>
        </select>
      </div>
      <div id="Hidden" class="form-group Hidden">
        <label>Hidden</label>
        <select name="hidden" data-initial="">
          <option value="">--</option>
          <option value="true">True</option>
          <option value="false">False</option>
        </select>
      </div>
    </form>
    `),button:"Submit",success:function(){let i=e("#users-bulk-edit").serializeJSON(!0);const o=[];for(var n of t)o.push(l.fetch(`/api/v1/users/${n}`,{method:"PATCH",body:JSON.stringify(i)}));Promise.all(o).then(p=>{window.location.reload()})}}),document.querySelector("#is_jury").value==="true"&&(document.querySelector("#Verified").style.display="none",document.querySelector("#Hidden").style.display="none")}e(()=>{e("#users-delete-button").click(d),e("#users-edit-button").click(c)});
