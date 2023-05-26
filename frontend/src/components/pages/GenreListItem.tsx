import React, { useContext } from "react";
import { Link, useRouteMatch } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";
import { Genre } from "../../CustomTypes";
import "../style.css"; // Import the Genres CSS file
import LibrarianLinks from "../LibrarianLinks";

export type GenreListItemProps = {
  key: number;
  item: Genre;
  linksto: string;
};

function GenreListItem(props: GenreListItemProps) {
  const { url }: { url: string } = useRouteMatch();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

  return (
    <>
      <Link to={props.linksto}>{props.item.genre}</Link>
      {isLibrarian === true ? (
        <LibrarianLinks url={`genre/${props.item.id}`} />
      ) : null}
    </>
  );
}

export default GenreListItem;
