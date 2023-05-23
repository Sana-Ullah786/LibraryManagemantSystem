import { ReactElement, useEffect, useState } from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { client } from "../axios";
import {
  Author,
  BookOut,
  BookIn,
  Genre,
  Language,
  CopyIn,
  CopyOut,
  Status,
} from "../CustomTypes";
import "./style.css"; // Import the Genres CSS file

/**
 * The BookForm component displays a form for getting all book details from user.
 * @param props The properties that were passed to this component.
 * @returns The rendered component.
 */
function CopyForm(props: {
  copy: CopyIn;
  submitHandler: SubmitHandler<CopyOut>;
}): ReactElement {
  console.log(props.copy);
  // A form for book
  let { register, handleSubmit } = useForm<CopyOut>({
    defaultValues: {
      statusId: props.copy.status.id,
      languageId: props.copy.language.id,
      bookId: props.copy.book.id,
    },
  });

  // Details of all languages present in the system.
  let [languages, setLanguages]: [
    Language[] | undefined,
    React.Dispatch<React.SetStateAction<Language[] | undefined>>
  ] = useState();

  let [statuses, setStatuses]: [
    Status[] | undefined,
    React.Dispatch<React.SetStateAction<Status[] | undefined>>
  ] = useState();

  // This effect fetches languages from backend
  useEffect(() => {
    client.GetAllLanguages().then(
      (languages: Language[]) => {
        setLanguages(languages);
      },
      (error) => {
        console.log(`Error! couldn't fetch languages`);
      }
    );
    client.GetAllStatuses().then(
      (statusList: Status[]) => {
        setStatuses(statusList);
      },
      (error) => {
        console.log(`Error! couldn't fetch statuses`);
      }
    );
  }, []);

  return (
    <div className="signup-container">
      <form
        className="signup-form"
        onSubmit={handleSubmit(props.submitHandler)}
      >
        <label className="form-group">
          {" "}
          Language
          {
            /* A dropdown menu for selecting from all languages */
            languages && (
              <select
                {...register("languageId")}
                id="languages"
                defaultValue={props.copy.language.id}
              >
                {languages.map((language) => {
                  return (
                    <option value={language.id} key={language.id}>
                      {" "}
                      {language.language}{" "}
                    </option>
                  );
                })}
              </select>
            )
          }
          {!languages && <>No Languages!</>}
        </label>
        <label className="form-group">
          {" "}
          Status
          {
            /* A dropdown menu for selecting from all languages */
            statuses && (
              <select
                {...register("statusId")}
                id="statuses"
                defaultValue={props.copy.status.id}
              >
                {statuses.map((status) => {
                  return (
                    <option value={status.id} key={status.id}>
                      {" "}
                      {status.status}{" "}
                    </option>
                  );
                })}
              </select>
            )
          }
          {!statuses && <>No statuses!</>}
        </label>
        <button>Submit</button>
      </form>
    </div>
  );
}

export default CopyForm;
