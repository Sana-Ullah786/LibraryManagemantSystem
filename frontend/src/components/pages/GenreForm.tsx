// GenreForm.tsx
import React from 'react';
import { useForm } from 'react-hook-form';

interface Props {
  genre: string | null | undefined;
  onSubmit: (data: { id: number; genre: string  }) => void;
}

function GenreForm({ genre, onSubmit }: Props) {
  const { handleSubmit, register } = useForm();

  const handleFormSubmit = (data: { genre: string }) => {
    onSubmit({ id: 0, genre: data.genre });
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <label>
        Genre:
        <input type="text" defaultValue={genre !== null ? genre : ''} {...register('genre')} />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default GenreForm;
