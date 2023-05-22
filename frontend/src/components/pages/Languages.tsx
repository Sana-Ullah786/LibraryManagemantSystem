import React, { useEffect, useState, useContext } from 'react';
import { client } from '../../axios';
import LanguageListItem from './LanguageListitem';
import { Link, useRouteMatch } from 'react-router-dom';
import { AuthContext } from '../../contexts/AuthContext';
import { Language, ErrorObject } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import "../style.css"; // Import the Languages CSS file

function Languages() {
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

  let { url }: { url: string } = useRouteMatch();

  const [languageList, setLanguageList] = useState<Language[]>([]);
  const [error, setError] = useState<ErrorObject>();

  useEffect(() => {
    client.GetAllLanguages()
      .then((languageList) => {
        if (languageList) {
          setLanguageList(languageList);
        }
      })
      .catch((error) => {
        setError(error);
      });
  }, []);

  function setLanguageListItemComponent(languageList: Language[]) {
    const languageListItemComponent: JSX.Element[] = languageList.map((language) => (
      <li className="language-list-item" key={language.id}>
        <LanguageListItem key={language.id} item={language} linksto={`${url}/${language.id}`} />
      </li>
    ));
    return languageListItemComponent;
  }

  function createLanguageLink() {
    return (
      <Link to={`${url}/create`} className="genre-link">
        Create Language
      </Link>
    );
  }

  if (error != null) {
    return (
      <ErrorComponent error={error} />
    );
  }

  return (
    <div>
      <h1>Language List</h1>
      <ul className="language-list">
        {setLanguageListItemComponent(languageList)}
      </ul>
      {isLibrarian ? createLanguageLink() : null}
    </div>
  );
}

export default Languages;
