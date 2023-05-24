import { ReactElement, useEffect, useState } from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { client } from "../axios";
import {
  Author,
  BookOut,
  BorrowedIn,
  BorrowedOut,
  Genre,
  Language,
} from "../CustomTypes";
import "./style.css"; // Import the Genres CSS file

function BorrowForm(props: {
  borrowed: BorrowedIn;
  isLibrarian: boolean;
  submitHandler: SubmitHandler<BorrowedOut>;
}): ReactElement {
  // A form for book
  let { register, handleSubmit } = useForm<BorrowedOut>({
    defaultValues: {
      ...props.borrowed,
      copyId: props.borrowed.copy.id,
      userId: props.borrowed.user.id,
    },
  });

  return (
    <div className="signup-container">
      <h1>Borrowing {props.borrowed.copy.book.title}</h1>
      <form
        className="signup-form"
        onSubmit={handleSubmit(props.submitHandler)}
      >
        <label className="form-group">
          Issue Date
          <input {...register("issueDate")} type="datetime-local" readOnly />
        </label>
        <br></br>
        <label className="form-group">
          Due Date
          <input {...register("dueDate")} type="datetime-local" />
        </label>
        <br></br>
        {props.isLibrarian && (
          <>
            <label className="form-group">
              Return Date
              <input {...register("returnDate")} type="date" />
            </label>
            <br></br>
          </>
        )}
        <button>Submit</button>
      </form>
    </div>
  );
}

export default BorrowForm;
