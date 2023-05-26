import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Language } from "../../CustomTypes";
import "../style.css"; // Import the Languages CSS file
import LibrarianLinks from "../LibrarianLinks";
import { AuthContext } from "../../contexts/AuthContext";

interface LanguageListItemProps {
  item: Language;
  linksto: string;
}

const LanguageListItem: React.FC<LanguageListItemProps> = ({
  item,
  linksto,
}) => {
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  return (
    <>
      <Link to={linksto}> {item.language}</Link>
      {isLibrarian && <LibrarianLinks url={`/Language/${item.id}`} />}
    </>
  );
};

export default LanguageListItem;
