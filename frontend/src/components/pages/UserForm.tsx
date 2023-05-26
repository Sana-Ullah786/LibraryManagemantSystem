import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { UserDetails } from "../../CustomTypes";

interface Props {
  user: UserDetails | null;
  onSubmit: SubmitHandler<UserDetails>;
}

function UserForm({ user, onSubmit }: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UserDetails>();

  const submitForm: SubmitHandler<UserDetails> = (data) => {
    onSubmit(data);
  };

  return (
    <div className="modal">
      <form onSubmit={handleSubmit(submitForm)}>
        <div className="signup-container">
          <div>
            <label className="form-group" htmlFor="email">
              Email:
            </label>
            <input
              type="email"
              id="email"
              defaultValue={user?.email || ""}
              {...register("email", { required: true })}
            />
            {errors.email && <span>This field is required</span>}
          </div>

          <div>
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              defaultValue={user?.username || ""}
              {...register("username", { required: true })}
            />
            {errors.username && <span>This field is required</span>}
          </div>

          <div>
            <label htmlFor="password">New Password:</label>
            <input
              type="password"
              id="password"
              defaultValue={user?.password || ""}
              {...register("password", { required: true })}
            />
            {errors.password && <span>This field is required</span>}
          </div>
          <div>
            <label htmlFor="old_password"> Old Password:</label>
            <input
              type="password"
              id="old_password"
              placeholder="Required"
              {...register("old_password", { required: true })}
            />
            {errors.password && <span>This field is required</span>}
          </div>
          <div>
            <label htmlFor="firstName">First Name:</label>
            <input
              type="text"
              id="firstName"
              defaultValue={user?.first_name || ""}
              {...register("first_name", { required: true })}
            />
            {errors.first_name && <span>This field is required</span>}
          </div>

          <div>
            <label htmlFor="lastName">Last Name:</label>
            <input
              type="text"
              id="lastName"
              defaultValue={user?.last_name || ""}
              {...register("last_name", { required: true })}
            />
            {errors.last_name && <span>This field is required</span>}
          </div>

          <div>
            <label htmlFor="contactNumber">Contact Number:</label>
            <input
              type="tel"
              id="contactNumber"
              defaultValue={user?.contact_number || ""}
              {...register("contact_number", { required: true })}
            />
            {errors.contact_number && <span>This field is required</span>}
          </div>

          <div>
            <label htmlFor="address">Address:</label>
            <textarea
              id="address"
              defaultValue={user?.address || ""}
              {...register("address", { required: true })}
            />
            {errors.address && <span>This field is required</span>}
          </div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
}

export default UserForm;
