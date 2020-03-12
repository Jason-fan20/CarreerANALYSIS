var nodes = (function() {
  var icount;
  var circle_radius = 5;
  var color_l=[]
	
 var _3c = (function() {
 var array=[];
 for(var i=0;i<d3.schemeCategory20.length;i++){
      array.push(d3.schemeCategory20[i]) 
}
for(var i=0;i<d3.schemeCategory20b.length;i++){
      array.push(d3.schemeCategory20b[i]) 
}
for(var i=0;i<d3.schemeCategory20c.length;i++){
      array.push(d3.schemeCategory20c[i]) 
}
return array;
})
  var color = d3.scaleOrdinal(_3c()).domain(["zero", "Institutional point","外交", "国防", "发展和改革委员会", "教育", "科学技术", "工业和信息化", "民族家族事物", "公安", "国家安全", "民政", "司法", "财政", "人力资源", "自然资源", "生态环境", "住房", "交通运输", "水利", "农业农村", "商务", "文化", "卫生健康", "退役军人", "消防", "银行", "审计", "国有资产监督管理", "海关", "税务", "市场监督", "广播电视", "体育", "统计", "国际发展合作", "医疗保障", "参事", "机关事务管理", "信访", "粮食物资储备", "能源", "国防科技", "烟草", "移民", "林业和草原", "铁路", "航空", "邮政", "文物", "医药管理", "煤矿监察", "外汇管理", "药品监督", "知识产权", "部队", "高等院校", "社会保障", "党", "机关"]);
  str=["外交", "国防", "发展和改革委员会", "教育", "科学技术", "工业和信息化", "民族家族事物", "公安", "国家安全", "民政", "司法", "财政", "人力资源", "自然资源", "生态环境", "住房", "交通运输", "水利", "农业农村", "商务", "文化", "卫生健康", "退役军人", "消防", "银行", "审计", "国有资产监督管理", "海关", "税务", "市场监督", "广播电视", "体育", "统计", "国际发展合作", "医疗保障", "参事", "机关事务管理", "信访", "粮食物资储备", "能源", "国防科技", "烟草", "移民", "林业和草原", "铁路", "航空", "邮政", "文物", "医药管理", "煤矿监察", "外汇管理", "药品监督", "知识产权", "部队", "高等院校", "社会保障", "党", "机关"];		
  		str.map(function(thing) {
		//console.log(thing);
		//console.log(color(thing));
		})
  this.clear = function() {
    //color = d3.scaleOrdinal(d3.schemeCategory10);
  }

  var circle_click = function(graph, member) {
    if (!d3.event.shiftKey) {
      selection.clear();
      member_lines.clear();
    }

    var draw_member_lines = true;

    if (selection.size() > 0) {
      member_lines.clear();
      draw_member_lines = false;
    }

    var group = graph.nodes[graph.group_map[graph.member_map[member.id].group]];

    selection.add(member);

    if (!draw_member_lines) {
      selection.clear_contacts();
      return;
    }

    var start_x = group.x + member.circle.attr('cy')*1;
    var start_y = group.y + member.circle.attr('cx')*1;

    for (var cid in graph.all_links[member.id]) {
      var contact_member = graph.member_map[cid];
      var contact_group = graph.nodes[graph.group_map[contact_member.group]];

      // They are in the same group.
      if (contact_member.group === member.group) { continue }

      var end_x = contact_group.x + contact_member.cx;
      var end_y = contact_group.y + contact_member.cy;


      member_lines.add(start_x, start_y, end_x, end_y);
      selection.add(contact_member, 'contact');
    }
  };

  var generateWedgeString = function(startX, startY, startAngle, endAngle, radius){
      var x1 = (startX + radius * Math.cos(Math.PI * startAngle/180)).toFixed(4);
      var y1 = (startY + radius * Math.sin(Math.PI * startAngle/180)).toFixed(4);
      var x2 = (startX + radius * Math.cos(Math.PI * endAngle/180)).toFixed(4);
      var y2 = (startY + radius * Math.sin(Math.PI * endAngle/180)).toFixed(4);
      var pathString = "M"+ startX + " " + startY + " L" + x1 + " " + y1 + " A" + radius + " " + radius + " 0 0 1 " + x2 + " " + y2 + " z";
      return pathString;
  }

  this.create_pie = function(graph, g, member, index, total) {
    var node = g.append('g').attr('class', 'membernode').attr('id', member.id)
      .attr('fill', color(member.type))
      .attr('name', 'default').on("click", function() {
        circle_click(graph, member);
		
      });

    var start = 90;
    var degrees = 360 / total;
    var start_deg = start + degrees * index;
    var end_deg = start + degrees * (index + 1);

    var arc = node.append("path").attr("d", generateWedgeString(0, 0, start_deg, end_deg, 5))
      .attr("class", "member");

    member.circle = arc;

    node.radius = function() {
      return 5;
    }

    node.set_position = function(x, y) {
      //
    };

    return node;
  }

  this.create_node = function(graph, g, member, scale) {
  //console.log(g);
    var node = g.append('g').attr('class', 'membernode').attr('id', member.id)
      .attr('fill', color(member.type))
      .attr('name', 'default').on("click", function() {
        circle_click(graph, member);
		console.log(member.type);
		console.log(typeof member.type);
      });
	node=node.on("mouseover", function() {
		document.getElementById('Node_information').innerHTML=member.circle['_groups'][0][0]['__data__'].details;
		})
	node=node.on("mouseout", function() {
		})
    var background = node.append("circle").attr("r", circle_radius * scale)
      .attr("class", "member-background");

    var circle = node.append("circle").attr("r", circle_radius * scale)
      .attr("class", "member");

    node.radius = function() {
      return circle_radius * scale;
    }

    member.circle = circle;

    node.set_position = function(x, y) {
      circle.attr('cx', x);
      circle.attr('cy', y);
      background.attr('cx', x);
      background.attr('cy', y);
    };

    return node;
  };

  return this;
})();
