{% macro get_models_latest_invocations_data() %}
  {% set invocations_relation = ref("elementary", "dbt_invocations") %}
  {% set column_exists = elementary.column_exists_in_relation(invocations_relation, 'job_url') %}

  {% set query %}
    with ordered_run_results as (
      select
        run_results.*,
        row_number() over (partition by run_results.unique_id order by run_results.generated_at desc) as row_number
      from {{ ref("elementary", "dbt_run_results") }} run_results
      join {{ ref("elementary", "dbt_models") }} models
      ON run_results.unique_id = models.unique_id
    ),

    latest_models_invocations as (
      select distinct invocation_id
      from ordered_run_results
      where row_number = 1
    )

    select
      invocations.invocation_id,
      command,
      selected,
      full_refresh,
      {% if column_exists %}
        job_url,
      {% endif %}
      job_name,
      job_id,
      orchestrator
    from {{ invocations_relation }} invocations
    join latest_models_invocations 
    ON invocations.invocation_id = latest_models_invocations.invocation_id
  {% endset %}
  {% set result = elementary.run_query(query) %}
  {% do return(elementary.agate_to_dicts(result)) %}
{% endmacro %}
