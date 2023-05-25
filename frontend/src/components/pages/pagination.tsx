import React, { ReactElement } from "react";

export type Props = {
  page: number;
  setPage: React.Dispatch<React.SetStateAction<number>>;
  showNext: boolean;
};

export function Pagination(props: Props): ReactElement {
  console.log(props.showNext);
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        marginLeft: 20,
        marginRight: 20,
      }}
    >
      <div>
        <button
          id="prev"
          onClick={() => {
            props.setPage(props.page - 1);
          }}
          className={props.page !== 1 ? "genre-link" : "genre-link-disabled"}
          disabled={props.page === 1}
        >
          {" "}
          Prev{" "}
        </button>
      </div>
      <div>Page {props.page}</div>
      <div>
        <button
          onClick={() => {
            props.setPage(props.page + 1);
          }}
          className={props.showNext ? "genre-link" : "genre-link-disabled"}
          disabled={!props.showNext}
        >
          {" "}
          Next{" "}
        </button>
      </div>
    </div>
  );
}
