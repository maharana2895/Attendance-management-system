$(function () {/*
Document loading, executing a function*/
    console.log("dasdasdsadsa")
    $('#defaultForm')
        .bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                /*input Status style picture*/
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                /*Verification: Rules*/
                username: {//Verify input: validation rules
                    message: 'The username is not valid',

                    validators: {
                        notEmpty: {//Non-empty verification: prompt message
                            message: 'Username can not be empty'

                        },
                        stringLength: {
                            min: 1,
                            max: 20,
                            message: 'Username must be between 1 and 20'
                        },
                        threshold: 1, //Send ajax request with more than 1 character. (Enter a character in input, the plugin will send it to the server once, set the limit, start with 1 character or more)
                        remote: {//ajax verification。server result:{"valid",true or false} Send current to the service input name Value, get a json data. The example is correct:{"valid",true}
                           url: '/register/',//Verify address
                            message: 'User already exists',//Prompt message
                            delay: 2000,//Every time you enter a character, you will send an ajax request, the server pressure is still too large, set a second to send ajax (default input one character, submit once, server pressure is too large)
                            type: 'POST',//Request method
                            /**Customize submission data, default values ​​are submitted to current input value*/
                            data: function(t) {

                               return {
                                   stu_num_verify: $('[name="stu_num"]').val()
                                   // whatever: $('[name="whateverNameAttributeInYourForm"]').val()
                               };
                            }

                        },
                        regexp: {
                            regexp: /^.+$/,
                            message: ''
                        }
                    }
                },
                password: {
                    message: 'Invalid password',
                    validators: {
                        notEmpty: {
                            message: 'password can not be blank'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: 'Password must be between 6 and 30'
                        },
                        identical: {//the same
                            field: 'password', //Need to compare input name value
                            message: 'Two passwords are inconsistent'
                        },
                        different: {//Cannot be the same as the username
                            field: 'username',//Need to compare input name value
                            message: 'Cannot be the same as the username'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: 'The username can only consist of alphabetical, number, dot and underscore'
                        }
                    }
                },
                repassword: {
                    message: 'Invalid password',
                    validators: {
                        notEmpty: {
                            message: 'password can not be blank'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: 'Password must be between 6 and 30'
                        },
                        identical: {//the same
                            field: 'password',
                            message: 'Two passwords are inconsistent'
                        },
                        different: {//Cannot be the same as the username
                            field: 'username',
                            message: 'Cannot be the same as the username'
                        },
                        regexp: {//Matching rule
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: 'The username can only consist of alphabetical, number, dot and underscore'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: 'Mail cannot be empty'
                        },
                        emailAddress: {
                            message: 'Please enter the correct email address as：123@qq.com'
                        }
                    }
                },
                phone: {
                    message: 'The phone is not valid',
                    validators: {
                        notEmpty: {
                            message: 'Phone number can not be blank'
                        },
                        stringLength: {
                            min: 11,
                            max: 11,
                            message: 'Please enter 11 mobile phone number'
                        },
                        regexp: {
                            regexp: /^1[0|3|5|8|9|6|7]{1}[0-9]{9}$/,
                            message: 'Please enter the correct phone number'
                        }
                    }
                },
                stu_num: {
                    message: 'The student number is not valid',
                    validators: {
                        notEmpty: {
                            message: 'Student number cannot be empty'
                        },
                        stringLength: {
                            min: 11,
                            max: 11,
                            message: 'Please enter 11 student numbers (less than 11 first places are filled with x)'
                        },
                        regexp: {
                            regexp: /^(x?[0-9]){10}|([0-9]{11})$/,
                            message: 'Please enter the correct student number'
                        }
                    }
                },
                invite: {
                    message: 'Invitation code',
                    validators: {
                        notEmpty: {
                            message: 'Invitation code cannot be empty'
                        },
                        stringLength: {
                            min: 8,
                            max: 8,
                            message: 'Please enter the correct length of the invitation code'
                        },
                        regexp: {
                            regexp: /^[\w]{8}$/,
                            message: 'Please enter the correct invitation code (including alphanumeric characters)'
                        }
                    }
                },
            }
        })

        //Automatically trigger form validation
        .on('success.form.bv', function (e) {//After clicking submit
            // Prevent form submission
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data Submit to formIn the label action，result customize
            $.post('/register_verify/', $form.serialize(), function (result) {
//do something...
                if(result == 'OK'){
                    window.location.href='/login/'
                }
            });
        });
});