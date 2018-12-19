<template>
  <div class="propuesta-crear">
    <h1>Escriba su deducción</h1><br>
    <form action="">
		<div class="form-group">
		<label for=""><h4>Deducción</h4></label> &nbsp
        <input type="text" class="form-control-sm" v-model="propuestas.propuesta">   &nbsp 
		<button class="btn btn-primary" @click.prevent="guardarPropuesta" type="button" name="button">Agregar deducción</button>
		</div>
	</form>
	
    <div class="propuestas">
    <h1 class="h1">Listado de Deducciones</h1> <br>
    <div id="tablaarbol" class= "table-responsive">
        <table class="table table-bordered table-hover table-dark">
            <thead class="thead-dark">
            <tr>
                <td>ID </td>
                <td>Deducción </td>
                <td>Respuesta </td>
                <td>Opciones </td>
            </tr>
            </thead>
            <tbody>
            <tr id="proprow" v-for="propuesta in propuestas" >
                <td>{{propuesta.id}} </td>
                <td>{{propuesta.propuesta}} </td>
                <td class="play" @click="abc" :data-arbolres="propuesta.respuesta"> &#9658; </td>
                <td>
                    <a @click.prevent="eliminarPropuesta(propuesta.id)" href="#">Eliminar</a>
                </td>    
            </tr>
            </tbody>
        </table>
	</div>
  </div>
   <div id="tree-simple" class="" style="width: 100%; overflow: visible; height: auto"></div>
 </div>



</template>

<script>
import axios from 'axios'
export default{
    name:'propuesta-crear',
    data(){
        return {
            propuestas:{id:null,propuesta:''}
        }
    },
    methods:{

        guardarPropuesta(){
            var datos={
                propuesta:this.propuestas.propuesta,
                message:'guardado'
            }
        
            axios.post('http://127.0.0.1:8000/api/',datos).
            then((respuesta)=>{
                console.log(respuesta)
                location.reload()
                recargar
            })
            .catch((respuesta)=>{
                alert("ERROR!");
            })
        },
        abc (e) {
            var DibujaArb = function (nodo) {
                var nodeChildren = []
                if(nodo._left){
                    nodeChildren.push( DibujaArb (nodo._left));
                }
                if(nodo._right){
                    nodeChildren.push( DibujaArb (nodo._right));
                }
                return {text: { name: nodo.Deduc, 'data-desc': nodo.regla.replace("RuleType.","") }, children: nodeChildren} 
            }
            var aaa = JSON.parse(e.currentTarget.dataset.arbolres)
            var simple_chart_config = {
                chart: {
                    container: "#tree-simple"
                },
                
                nodeStructure: DibujaArb(aaa)
                
            }
            var my_chart = new Treant(simple_chart_config);
        },
        recargar(){
            axios.get('http://127.0.0.1:8000/api/all/').then((respuesta)=>{
            this.propuestas=respuesta.data
        })

        },
        eliminarPropuesta(id){
        axios.delete('http://127.0.0.1:8000/api/'+id+'/')
        .then((respuesta)=>{console.log(respuesta)
        this.recargar()})}
        
    },
    mounted(){
        axios.get('http://127.0.0.1:8000/api/all/').then((respuesta)=>{
            this.propuestas=respuesta.data
        })

    },
    data(){
        return {
            propuestas:[]
        }
    },
}
  //  var abc = function() {
    //    alert("aaaa")
  //  }
    //var x = document.getElementsByClassName("prop-row");
    //addEventListener("click", myScript);
    //alert("aa")
</script>
