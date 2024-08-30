from services.encryption import encrypt_all_files_in_directory, decrypt_all_files_in_directory
from services.graphical_analyses import plot_activity_over_time, plot_top_activities, plot_monthly_activity_heatmap, \
    plot_activity_distribution, plot_cumulative_activity, plot_monthly_totals_comparison
from services.process_and_store_input import process_cards, extract_and_save_data_by_month

if __name__ == "__main__":
            ## Process Input ##
    # processed_cards = process_cards("encrypted_raw_data/Apr-Dec-2023.json")
    # extract_and_save_data_by_month(processed_cards)

            ## Encryption ##
    # Encrypt all JSON files in the directory
    encrypt_all_files_in_directory(
        directory='encrypted_raw_data',
        password='REDACTED'
    )

    # Decrypt all encrypted files in the directory
    decrypt_all_files_in_directory(
        input_directory='encrypted_raw_data',
        output_directory='raw_data',
        password='REDACTED'
    )

            ## Graphical Analyses ##
    # plot_activity_over_time('encrypted_data')             # ick
    # plot_top_activities('encrypted_data', 10)             # interesting
    # plot_monthly_activity_heatmap('encrypted_data')       # errors
    # plot_activity_distribution('encrypted_data')          # ick
    # plot_cumulative_activity('encrypted_data')            # meh
    # plot_monthly_totals_comparison('encrypted_data')      # interesting

    # TODO - refactor because I'm triggered
    pass