// This file is auto-generated by @hey-api/openapi-ts

import {
  type Options,
  createClient,
  createConfig,
} from "@hey-api/client-fetch";
import type {
  CreateGameData,
  CreateGameError,
  CreateGameResponse,
  CreateGuessData,
  CreateGuessError,
  CreateGuessResponse,
  CreateUserClientError,
  CreateUserClientResponse,
  ListCountriesError,
  ListCountriesResponse,
  ReadCountryData,
  ReadCountryError,
  ReadCountryResponse,
  ReadCurrentGameData,
  ReadCurrentGameError,
  ReadCurrentGameResponse,
  ReadGameData,
  ReadGameError,
  ReadGameResponse,
  ReadUserClientData,
  ReadUserClientError,
  ReadUserClientResponse,
  ReadUserStatsData,
  ReadUserStatsError,
  ReadUserStatsResponse,
} from "./types.gen";

export const client = createClient(createConfig());

export class DefaultService {
  /**
   * List Countries
   */
  public static listCountries<ThrowOnError extends boolean = false>(
    options?: Options<unknown, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<
      ListCountriesResponse,
      ListCountriesError,
      ThrowOnError
    >({
      ...options,
      url: "/countries",
    });
  }

  /**
   * Read Country
   */
  public static readCountry<ThrowOnError extends boolean = false>(
    options: Options<ReadCountryData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<
      ReadCountryResponse,
      ReadCountryError,
      ThrowOnError
    >({
      ...options,
      url: "/countries/{country_id}",
    });
  }

  /**
   * Create User Client
   */
  public static createUserClient<ThrowOnError extends boolean = false>(
    options?: Options<unknown, ThrowOnError>,
  ) {
    return (options?.client ?? client).post<
      CreateUserClientResponse,
      CreateUserClientError,
      ThrowOnError
    >({
      ...options,
      url: "/user_clients",
    });
  }

  /**
   * Read User Client
   */
  public static readUserClient<ThrowOnError extends boolean = false>(
    options: Options<ReadUserClientData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<
      ReadUserClientResponse,
      ReadUserClientError,
      ThrowOnError
    >({
      ...options,
      url: "/user_clients/{user_client_uuid}",
    });
  }

  /**
   * Read Current Game
   */
  public static readCurrentGame<ThrowOnError extends boolean = false>(
    options: Options<ReadCurrentGameData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<
      ReadCurrentGameResponse,
      ReadCurrentGameError,
      ThrowOnError
    >({
      ...options,
      url: "/user_clients/{user_client_uuid}/current_game",
    });
  }

  /**
   * Read User Stats
   */
  public static readUserStats<ThrowOnError extends boolean = false>(
    options: Options<ReadUserStatsData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<
      ReadUserStatsResponse,
      ReadUserStatsError,
      ThrowOnError
    >({
      ...options,
      url: "/user_clients/{user_client_uuid}/stats",
    });
  }

  /**
   * Create Game
   */
  public static createGame<ThrowOnError extends boolean = false>(
    options: Options<CreateGameData, ThrowOnError>,
  ) {
    return (options?.client ?? client).post<
      CreateGameResponse,
      CreateGameError,
      ThrowOnError
    >({
      ...options,
      url: "/games",
    });
  }

  /**
   * Read Game
   */
  public static readGame<ThrowOnError extends boolean = false>(
    options: Options<ReadGameData, ThrowOnError>,
  ) {
    return (options?.client ?? client).get<
      ReadGameResponse,
      ReadGameError,
      ThrowOnError
    >({
      ...options,
      url: "/games/{game_id}",
    });
  }

  /**
   * Create Guess
   */
  public static createGuess<ThrowOnError extends boolean = false>(
    options: Options<CreateGuessData, ThrowOnError>,
  ) {
    return (options?.client ?? client).post<
      CreateGuessResponse,
      CreateGuessError,
      ThrowOnError
    >({
      ...options,
      url: "/games/{game_id}/guesses",
    });
  }
}
