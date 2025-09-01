export default function useHelpers() {
  function catchErrorTyped<T, E extends new (message?: string) => Error>(
    promise: Promise<T>,
    errorsToCatch?: E[],
  ): Promise<[undefined, T] | [InstanceType<E>]> {
    return promise
      .then((data) => {
        return [undefined, data] as [undefined, T]
      })
      .catch((error) => {
        if (errorsToCatch === undefined) {
          return [error]
        }

        if (errorsToCatch.some((e) => error instanceof e)) {
          return [error]
        }

        if (errorsToCatch.some((e) => e.name === error.response?.data?.exception)) {
          const ExceptionConstructor = errorsToCatch.find((e) => e.name === e.name)

          if (ExceptionConstructor) {
            const customError = new ExceptionConstructor(error.response?.data?.detail)
            return [customError]
          }
        }

        return [error]
      })
  }

  return {
    catchErrorTyped,
  }
}