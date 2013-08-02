(function() {
    var comm_type_collection = new Backbone.Collection();

    //_.extend(comm_type_collection, Backbone.Events);

    comm_type_collection.on('render', function() {
	var area = Backbone.$('#commodity_type_manage > table > tbody');
	area.clear();

	_.for(this, function(iter) {
	    var tr = Backbone.$('<tr>');
	    tr.append(Backbone.$('<td>').text(iter['id']));
	    tr.append(Backbone.$('<td>').text(iter['type_name']));
	    tr.append(Backbone.$('<td>').text(iter['type_parent_id']));
	    area.append(tr);
	})
	
    }, comm_type_collection);

    comm_type_collection.on('refresh', function() {
	comm_type_collection.trigger('render');
    });
})()
