import math


class FilterPagination:

    '''
    # Custom Filter & Pagination
    @request: request (object), model_refrence (object)
    @response: dataset (dictionary)
    '''
    def filter_and_pagination(request, model_refrence):
        model_fields = [field.name for field in model_refrence._meta.get_fields()]
        filter_params = request.GET
        custom_filter = {}

        if filter_params:
            for k, v in filter_params.items():
                if k in model_fields:
                    if 'ForeignKey' == model_refrence._meta.get_field(k).get_internal_type():
                        custom_filter.update({k : v})
                    else:
                        custom_filter.update({k + '__icontains': v})

        if 'created_at_from' in filter_params:
            custom_filter.update({'created_at__gte': filter_params['created_at_from']})
        if 'created_at_to' in filter_params:
            custom_filter.update({'created_at__lte': filter_params['created_at_to']})
        if 'updated_at_from' in filter_params:
            custom_filter.update({'updated_at__gte': filter_params['updated_at_from']})
        if 'updated_at_to' in filter_params:
            custom_filter.update({'updated_at__lte': filter_params['updated_at_to']})

        queryset_filter = model_refrence.objects.filter(**custom_filter)
                    
        order_by_field = filter_params['order_by'] if (('order_by' in filter_params) and (filter_params['order_by'] in model_fields)) else 'id'
        order_type = '' if 'order_type' in filter_params else '-'
        order_by = order_type + order_by_field

        per_page = filter_params['per_page'] if 'per_page' in filter_params else 20
        page_no = filter_params['page_no'] if 'page_no' in filter_params else 1
    
        start_limit = ((int(per_page) * int(page_no)) - int(per_page))
        end_limit = int(per_page) * int(page_no)

        total_object_count = queryset_filter.count()
        total_pages = math.ceil( int(total_object_count) / int(per_page) )

        queryset = queryset_filter.order_by(order_by)[start_limit:end_limit]
        
        dataset = {
            'queryset': queryset,
            'pagination': {
                'per_page': per_page,
                'current_page': page_no,
                'total_count': total_object_count,
                'total_pages': total_pages
            }
        }
        return dataset