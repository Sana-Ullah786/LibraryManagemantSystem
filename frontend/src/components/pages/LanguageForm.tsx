import React from 'react';
import { useForm } from 'react-hook-form';
import "../style.css"; // Import the Languages CSS file

interface Props {
  language: string | null | undefined;
  onSubmit: (data: { id: number; language: string }) => void;
}

function LanguageForm({ language, onSubmit }: Props) {
  const { handleSubmit, register } = useForm();

  const handleFormSubmit = (data: { language: string }) => {
    onSubmit({ id: 0, language: data.language });
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <label>
        Language:
        <input
          type="text"
          defaultValue={language !== null ? language : ''}
          {...register('language')}
        />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default LanguageForm;
