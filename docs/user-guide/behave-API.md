# Behave API

Do HTTP API requests easily using Gherkin language.

---

**Note**: The code is available in the [steps.py](https://github.com/ivanprjcts/sdklib/tree/master/sdklib/test/behave/steps.py) module on GitHub.

---


## Step Catalog

### Given

* The API endpoint "{host}"
* The API proxy "{host}"
* The API resource "{url_path}"
* The parameterized API resource "/path/%(key1)s/to/%(key2)s" with these parameter values                 

 | key   | value  |  
 |---    | ---    |
 | key1  | value1 |
 | key2  | value2 | 

* Authorization-Basic with username "{username}" and password "{password}"
* 11Paths-Authorization with application id "{app_id}" and secret "{secret}"
* The headers

 | header_name   | header_value  |  
 |---    | ---    |
 | header1  	| value1       |
 | header2      | value2       |


* The query parameters

 | param_name   | param_value  |
 |---    | ---    |
 | param1  	| value1  	    |
 | param2 	| value2  	    |

* The body parameters

 | param_name   | param_value  |
 |---    | ---    |
 | param1  	| value1  	    |
 | param2 		| value2  	    |

* The body files

 | param_name   | param_value  |
 |---    | ---    |
 | param1  	| value1  	    |
 | param2 		| value2  	    |



### When

* I send a HTTP "{method}" request
* I send a HTTP "{method}" request with query parameters

 | param_name   | param_value  |
 |---    | ---    |
 | param1  	   | value1  	    |
 | param2            | value2  	    |

* I send a HTTP "{method}" request with body parameters

 | param_name   | param_value  |
 |---    | ---    |
 | param1  	   | value1  	    |
 | param2 	   | value2  	    |


### Then

* The HTTP status code should be "{code}"
* The HTTP status code should not be "{code}"
* The HTTP reason phrase should be "{phrase}"
* The HTTP reason phrase should contain "{phrase}"
* The response body should be this JSON:
```
	"""
	{
	    "param1": "value1",
	    "param2": "value2",
	    "param3":{
	   	 "param31": "value31"
	    }
	}
	"""
```

## Future

### When

* I send a HTTP "{method}" request with body parameters encoded "{encoding_type}"  # types: urlencoded, json, multipart, plain

 | param_name   | param_value  |
 |---    | ---    |
 | param1            | value1  	    |
 | param2            | value2  	    |


* I send a HTTP "{method}" request with this body "{resource_file}"


* I send a HTTP "{method}" request with this JSON
```
   	 """
   	 {
   		 "param1": "value1",
   		 "param2": "value2",
   		 "param3":{
   			 "param31": "value31"
   		 }
   	 }
   	 """
```
* I send a HTTP "{method}" request with this XML
```
   	 """
	 <xml>
	 	<key>
	 		<param1>Value1</param1>
		 	<param2>Value2</param2>
	 	</key>
	</xml>
	 """
```
### Then

* The response header "{header_name}" should be "{header_value}"
* The response header "{header_name}" should contain "{header_value}"
* The response body should contain this parameters:

 | param_name    | param_value  	 |
 |---    | ---    |
 | param1        | value1  		 |
 | param2  	 | value2   	 |

* The response body should be this "{response_file}"
* The response body should be this XML
```
   	 """
	 <xml>
	 	<key>
	 		<param1>Value1</param1>
		 	<param2>Value2</param2>
	 	</key>
	</xml>
	 """
```
