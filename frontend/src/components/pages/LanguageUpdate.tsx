import React, { ReactElement, useEffect, useState, useContext } from 'react';
import { client } from '../../axios';
import { useParams, useHistory } from 'react-router-dom';
import LanguageForm from './LanguageForm';
import { SubmitHandler } from 'react-hook-form';
import { ErrorObject, Language } from '../../CustomTypes';
import ErrorComponent from '../ErrorComponent';
import { AuthContext } from '../../contexts/AuthContext';

interface Props {}

function LanguageUpdate(props: Props): ReactElement {
  const { id }: { id: string } = useParams();
  const languageId: number = parseInt(id); // Parse id as a number
  const history = useHistory();

  const [language, setLanguage] = useState<string | null | undefined>();
  const [loaded, setLoaded] = useState<boolean>(false);
  const [error, setError] = useState<ErrorObject>();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } = useContext(AuthContext);

  useEffect(() => {
    client
      .GetLanguageDetails(id)
      .then((languageData) => {
        if (languageData) {
          setLanguage(languageData.language);
          setLoaded(true);
        }
      })
      .catch((error) => {
        setError(error);
      });
  }, [languageId]);

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

  const onSubmit: SubmitHandler<Language> = (data) => {

    client
      .PutLanguage(id, cleanData(data)) 
      .then((response) => {
        history.push('/language/' + languageId); 
      });   
  };

  function cleanData(data: Language) {
    data.language = data.language !== null ? data.language : '';
    return data;
  }

  if (error != null) {
    return <ErrorComponent error={error} />;
  }

  return (
    <div>
      {loaded === true ? (
        <LanguageForm language={language || ''} onSubmit={onSubmit} />
      ) : (
        <h1>--Loading--</h1>
      )}
    </div>
  );
}

export default LanguageUpdate;
