import{$ as e,e as d,C as l,A as u}from"./main-C4_GQfqy.js";function r(s){let t=e("input[data-team-id]:checked").map(function(){return e(this).data("team-id")}),i=t.length===1?"team":"teams";d({title:"Delete Teams",body:`Are you sure you want to delete ${t.length} ${i}?`,success:function(){const a=[];for(var o of t)a.push(l.fetch(`/api/v1/teams/${o}`,{method:"DELETE"}));Promise.all(a).then(n=>{window.location.reload()})}})}function c(s){let t=e("input[data-team-id]:checked").map(function(){return e(this).data("team-id")});u({title:"Edit Teams",body:e(`
    <form id="teams-bulk-edit">
      <div class="form-group">
        <label>Banned</label>
        <select name="banned" data-initial="">
          <option value="">--</option>
          <option value="true">True</option>
          <option value="false">False</option>
        </select>
      </div>
      <div id = "Hidden" class="form-group">
        <label>Hidden</label>
        <select name="hidden" data-initial="">
          <option value="">--</option>
          <option value="true">True</option>
          <option value="false">False</option>
        </select>
      </div>
    </form>
    
    `),button:"Submit",success:function(){let a=e("#teams-bulk-edit").serializeJSON(!0);const o=[];for(var n of t)o.push(l.fetch(`/api/v1/teams/${n}`,{method:"PATCH",body:JSON.stringify(a)}));Promise.all(o).then(m=>{window.location.reload()})}}),document.querySelector("#is_jury").value==="true"&&(document.querySelector("#Hidden").style.display="none")}e(()=>{e("#teams-delete-button").click(r),e("#teams-edit-button").click(c)});
