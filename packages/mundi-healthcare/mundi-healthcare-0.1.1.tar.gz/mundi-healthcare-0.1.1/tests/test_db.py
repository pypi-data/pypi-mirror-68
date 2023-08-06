from mundi import region

from mundi_healthcare import icu_capacity


class TestDb:
    def test_examples(self):
        br = region('BR')
        
        print(br.to_series(
            'icu_capacity',
            'hospital_capacity',
            'icu_capacity_public',
            'hospital_capacity_public',
        ))
        assert icu_capacity('BR') == br.icu_capacity
        assert br.icu_capacity == 59_695
        assert br.icu_capacity_public == 32_016
        assert br.hospital_capacity == 363_927
        assert br.hospital_capacity_public == 250_571

    def test_aggregate_values_from_municipalities(self):
        df = region('BR-DF')
        bsb, _, df_meso, df_micro, df_sus = xs = sorted(df.children(deep=True))
        del xs[1]  # no information about district
        print(xs)
        print(bsb)
        assert bsb.hospital_capacity > 0
        assert bsb.hospital_capacity_public > 0
        assert bsb.icu_capacity > 0
        assert bsb.icu_capacity_public > 0
        assert all(x.hospital_capacity == bsb.hospital_capacity for x in xs)
        assert all(x.hospital_capacity_public == bsb.hospital_capacity_public for x in xs)
        assert all(x.icu_capacity == bsb.icu_capacity for x in xs)
        assert all(x.icu_capacity_public == bsb.icu_capacity_public for x in xs)
