import React, { ReactElement } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { AuthorDetails } from "../CustomTypes";

/**
 * Extending the AuthorDetails interface to create the props interface,
 * This is because we need to pass the author details seperately to the OnSubmit function.
 * The OnSubmit function itself is obtained as a prop from either the AuthorCreate or AuthotUpdate pages.
 * This allows the Author Form component to be used by both pages.
 */
interface Props extends AuthorDetails {
  onSubmit: SubmitHandler<AuthorDetails>;
}

function AuthorForm(props: Props): ReactElement {
  //We are using the useForm hook provided by the react-hook-form library
  //We can set the default values of the form by passing the desired values to the hook as shown
  const { register, handleSubmit } = useForm<AuthorDetails>({
    defaultValues: {
      first_name: props.first_name,
      last_name: props.last_name,
      birth_date: props.birth_date?.substring(0, 10),
      death_date: props.death_date?.substring(0, 10),
    },
  });

    return (
        <div className="signup-container">
            {/* We can pass our custom onSubmit function as an argument to the handleSubmit function provided by react hook forms */}
            <form  className="signup-form" onSubmit = {handleSubmit(props.onSubmit)}>
                <label className="form-group">First Name
                    {/* to use reacthook forms, we register the input field of the form as shown below by assigning it a name
                    The name must match the names provided in the DefaultValues defined above. If no DefaultValues are defined, the names
                    can be anything */}
          <input
            {...register("first_name")}
            type="text"
            placeholder={"First Name"}
          />
        </label>
        <br />
        <label>
          Last Name
          <input
            {...register("last_name")}
            type="text"
            placeholder={"Last Name"}
          />
        </label>
        <br />
        <label>
          Date of Birth
          <input {...register("birth_date")} type="date" />
        </label>
        <br />
        <label>
          Date Of Death
          <input {...register("death_date")} type="date" />
        </label>
        <br />
        <button>Submit</button>
      </form>
    </div>
  );
}

export default AuthorForm;
