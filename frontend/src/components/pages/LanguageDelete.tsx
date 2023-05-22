import React, { ReactElement, useEffect, useState, useContext } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { client } from '../../axios';
import { ErrorObject } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import { AuthContext } from '../../contexts/AuthContext';
import '../style.css'; // Import the Languages CSS file

interface Props {}

function LanguageDelete(props: Props): ReactElement {
  const { id }: { id: string } = useParams();
  const history = useHistory();
  const [language, setLanguage] = useState<string | null | undefined>('--Loading--');
  const [error, setError] = useState<ErrorObject>();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } = useContext(AuthContext);

  useEffect(() => {
    client
      .GetLanguageDetails(id)
      .then((languageData) => {
        setLanguage(languageData.language);
      })
      .catch((error) => {
        setError(error);
      });
  }, [id]);

  useEffect(() => {
    if (isAuthenticated === true) {
      if (isLibrarian !== true) {
        let err: ErrorObject = {
          status: 403,
          message: 'Forbidden. You do not have permission to view this page',
        };
        setError(err);
      }
    } else {
      let err: ErrorObject = {
        status: 401,
        message: 'Unauthorized, you must be logged in to view this page',
      };
      setError(err);
    }
  }, [isAuthenticated, isLibrarian]);

  function handleDelete() {
    client
      .DeleteLanguage(id)
      .then((response) => {
        history.push('/language');
      });
  }

  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div>
      <h1>Delete Language: {language}</h1>
      <button onClick={handleDelete} className="language-list-danger-button">
        Yes, Delete
      </button>
    </div>
  );
}

export default LanguageDelete;
